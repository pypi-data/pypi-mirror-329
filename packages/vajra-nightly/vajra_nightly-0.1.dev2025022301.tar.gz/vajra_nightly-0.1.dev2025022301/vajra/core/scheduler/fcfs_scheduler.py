from typing import Any, Dict, List

from vidur.config import RandomForrestExecutionTimePredictorConfig, ReplicaConfig
from vidur.entities import Batch as VidurBatch
from vidur.execution_time_predictor import ExecutionTimePredictorRegistry
from vidur.execution_time_predictor.base_execution_time_predictor import (
    BaseExecutionTimePredictor,
)

from vajra.core.scheduler.base_scheduler import BaseScheduler, BatchFormationTracker
from vajra.datatypes import Sequence

PREDICTION_MAX_CHUNK_SIZE = 4 * 1024
MAX_TOKENS_PER_SEQ = 2 * 1024 * 1024
PREDICTION_MAX_BATCH_SIZE = 128
PREDICTION_DEVICE = "h100"
PREDICTION_NETWORK_DEVICE = "h100_dgx"
# PREDICTION_DEVICE = "a100"
# PREDICTION_NETWORK_DEVICE = "a100_dgx"
KV_CACHE_PREDICTION_GRANULARITY = 512
MODEL_NAME_MAPPING = {
    "meta-llama/Meta-Llama-3-8B": "meta-llama/Meta-Llama-3-8B",
    "meta-llama/Meta-Llama-3-8B-Instruct": "meta-llama/Meta-Llama-3-8B",
    "gradientai/Llama-3-8B-Instruct-Gradient-1048k": "meta-llama/Meta-Llama-3-8B",
    "gradientai/Llama-3-70B-Instruct-Gradient-1048k": "meta-llama/Meta-Llama-3-70B",
}

EXECUTION_TIME_PREDICTION_SLACK = 0.1
EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE = 512
EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY = 32


def round_down_to_nearest_multiple(value: int, multiple: int) -> int:
    return (value // multiple) * multiple


def round_up_to_nearest_multiple(value: int, multiple: int) -> int:
    return ((value + multiple - 1) // multiple) * multiple


class BatchFormationTrackerWithRuntimePrediction(BatchFormationTracker):
    def __init__(
        self,
        schedule_id: int,
        max_micro_batch_size: int,
        pipeline_parallel_size: int,
        kv_parallel_size: int,
        max_num_tokens_per_kvp_group: int,
        max_chunk_size: int,
        min_chunk_size: int,
        execution_time_predictor: BaseExecutionTimePredictor,
    ):
        super().__init__(
            schedule_id,
            max_micro_batch_size,
            kv_parallel_size,
            max_num_tokens_per_kvp_group,
        )
        self.pipeline_parallel_size = pipeline_parallel_size
        self.execution_time_predictor = execution_time_predictor
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

        self.batch_execution_time_predictions: List[int] = [
            0 for _ in range(self.kv_parallel_size)
        ]

    def add_sequence(
        self,
        seq: Sequence,
        num_q_tokens: int,
        active_kvp_group_ids: List[int],
        kvp_group_block_counter: Dict[int, int],
    ) -> None:
        super().add_sequence(
            seq, num_q_tokens, active_kvp_group_ids, kvp_group_block_counter
        )

        if num_q_tokens == 1:
            # Do not update predictions for decode seqs
            # We are assuming that the decode seqs are all added
            # at the beginning and don't need q chunk sizes, so we can just
            # do updates once we start adding prefills
            return

        for kvp_group_id in range(self.kv_parallel_size):
            self.batch_execution_time_predictions[kvp_group_id] = (
                self._compute_batch_execution_time(kvp_group_id)
            )

    def _compute_batch_execution_time(
        self,
        kvp_group_id: int,
        extra_seqs: List[Sequence] = [],
        extra_num_q_tokens: List[int] = [],
        extra_num_kv_tokens: List[int] = [],
        extra_num_active_kvp_groups: List[int] = [],
        extra_last_kvp_group_ids: List[int] = [],
    ) -> int:
        if len(self.per_kvp_group_sequences[kvp_group_id]) + len(extra_seqs) == 0:
            return 0

        num_seqs = len(self.per_kvp_group_sequences[kvp_group_id]) + len(extra_seqs)

        return (
            self.execution_time_predictor.get_execution_time(
                VidurBatch(
                    0,  # replica_id
                    [None] * num_seqs,  # sequences
                    self.per_kvp_group_num_q_tokens[kvp_group_id] + extra_num_q_tokens,
                    self.per_kvp_group_num_kv_tokens[kvp_group_id]
                    + extra_num_kv_tokens,
                    self.per_kvp_group_num_active_kvp_groups[kvp_group_id]
                    + extra_num_active_kvp_groups,
                    self.per_kvp_group_last_kvp_group_ids[kvp_group_id]
                    + extra_last_kvp_group_ids,
                    kvp_group_id,
                ),
                pipeline_stage=0,
            ).total_time
            * self.pipeline_parallel_size
        )

    def get_batch_execution_time(self, kvp_group_id: int) -> int:
        return self.batch_execution_time_predictions[kvp_group_id]

    def get_batch_execution_time_for_kvp_groups(self, kvp_group_ids: List[int]) -> int:
        return [
            self.batch_execution_time_predictions[kvp_group_id]
            for kvp_group_id in kvp_group_ids
        ]

    def get_max_chunk_size_for_seq(
        self,
        seq: Sequence,
        active_kvp_group_ids: List[int],
        target_batch_time: float,
    ) -> int:
        # identify the kvp group with the maximum execution time, and get the execution time and group id
        max_execution_time_group_id = active_kvp_group_ids[0]
        max_execution_time = 0

        for kvp_group_id in active_kvp_group_ids:
            execution_time = self.get_batch_execution_time(kvp_group_id)
            if execution_time > max_execution_time:
                max_execution_time = execution_time
                max_execution_time_group_id = kvp_group_id

        if max_execution_time > target_batch_time * (
            1 - EXECUTION_TIME_PREDICTION_SLACK
        ):
            return 0

        is_last_group = max_execution_time_group_id == active_kvp_group_ids[-1]

        num_processed_tokens = seq.get_num_tokens_stage_processed()

        num_kv_tokens = self._get_num_kv_tokens(
            num_processed_tokens, active_kvp_group_ids, is_last_group
        )
        num_kvp_groups = len(active_kvp_group_ids)
        last_kvp_group_id = active_kvp_group_ids[-1]
        remaining_tokens = max(seq.prompt_len - num_processed_tokens, 0)

        # Get initial bounds for binary search
        if hasattr(seq, "__last_chunk_size"):
            high = seq.__last_chunk_size
        else:
            high = EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE

        # Cap high by remaining tokens
        high = round_down_to_nearest_multiple(
            2 * high, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY
        )
        high = min(remaining_tokens, high)
        low = 0

        # Binary search with 32-token steps except for last chunk
        closest_match = 0
        closest_time = None

        seen_chunk_sizes = set()

        while low <= high:
            mid = (low + high) // 2

            mid = min(self.max_chunk_size, mid)

            if mid < remaining_tokens:
                mid = round_down_to_nearest_multiple(
                    mid, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY
                )
                if mid == 0:
                    mid = min(self.min_chunk_size, remaining_tokens)
            else:
                mid = remaining_tokens

            if mid in seen_chunk_sizes:
                break

            seen_chunk_sizes.add(mid)

            if mid == 0:
                break

            execution_time = self._compute_batch_execution_time(
                max_execution_time_group_id,
                extra_seqs=[seq],
                extra_num_q_tokens=[mid],
                extra_num_kv_tokens=[num_kv_tokens],
                extra_num_active_kvp_groups=[num_kvp_groups],
                extra_last_kvp_group_ids=[last_kvp_group_id],
            )

            # Check if execution time is within both bounds of slack range
            if execution_time >= target_batch_time * (
                1 - EXECUTION_TIME_PREDICTION_SLACK
            ) and execution_time <= target_batch_time * (
                1 + EXECUTION_TIME_PREDICTION_SLACK
            ):
                # Found a good size within slack range
                closest_match = mid
                closest_time = execution_time
                break
            elif execution_time < target_batch_time * (
                1 - EXECUTION_TIME_PREDICTION_SLACK
            ):
                low = mid
            else:
                high = mid

            if closest_time is None or abs(execution_time - target_batch_time) < abs(
                closest_time - target_batch_time
            ):
                closest_match = mid
                closest_time = execution_time

        if closest_match != 0:
            seq.__last_chunk_size = closest_match

        return closest_match


class FcfsScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        execution_time_predictor_config = RandomForrestExecutionTimePredictorConfig(
            prediction_max_prefill_chunk_size=PREDICTION_MAX_CHUNK_SIZE,
            prediction_max_tokens_per_request=MAX_TOKENS_PER_SEQ,
            prediction_max_batch_size=PREDICTION_MAX_BATCH_SIZE,
            kv_cache_prediction_granularity=KV_CACHE_PREDICTION_GRANULARITY,
        )
        replica_config = ReplicaConfig(
            model_name=MODEL_NAME_MAPPING[self.model_config.model],
            num_pipeline_stages=self.parallel_config.pipeline_parallel_size,
            tensor_parallel_size=self.parallel_config.tensor_parallel_size,
            kv_parallel_size=self.parallel_config.kv_parallel_size,
            max_num_tokens_per_kvp_group=self.parallel_config.max_num_tokens_per_kvp_group,
            enable_sequence_pipeline_parallel=self.parallel_config.enable_sequence_pipeline_parallel,
            device=PREDICTION_DEVICE,
            network_device=PREDICTION_NETWORK_DEVICE,
            block_size=self.cache_config.block_size,
        )
        self.execution_time_predictor = ExecutionTimePredictorRegistry.get(
            execution_time_predictor_config.get_type(),
            predictor_config=execution_time_predictor_config,
            replica_config=replica_config,
        )

    def _get_batch_formation_tracker(self) -> BatchFormationTracker:
        return BatchFormationTrackerWithRuntimePrediction(
            schedule_id=self._iteration_id,
            max_micro_batch_size=self.scheduler_config.max_batch_size,
            pipeline_parallel_size=self.parallel_config.pipeline_parallel_size,
            kv_parallel_size=self.parallel_config.kv_parallel_size,
            max_num_tokens_per_kvp_group=self.max_num_tokens_per_kvp_group,
            max_chunk_size=self.scheduler_config.max_chunk_size,
            min_chunk_size=self.scheduler_config.min_chunk_size,
            execution_time_predictor=self.execution_time_predictor,
        )

    def _get_seq_next_num_q_tokens(
        self, seq: Sequence, batch_formation_tracker: BatchFormationTracker
    ) -> int:
        assert not seq.is_finished()
        assert not seq.prompt_stage_processing_finished

        active_kvp_group_ids = self._get_active_kvp_group_ids(seq)

        next_num_tokens = batch_formation_tracker.get_max_chunk_size_for_seq(
            seq,
            active_kvp_group_ids,
            self.scheduler_config.target_batch_time,
        )

        num_processed_tokens = seq.get_num_tokens_stage_processed()
        if self.parallel_config.kv_parallel_size > 1:
            last_group_tokens = num_processed_tokens % self.max_num_tokens_per_kvp_group
            next_num_tokens = min(
                next_num_tokens,
                self.max_num_tokens_per_kvp_group - last_group_tokens,
            )

        next_num_tokens = max(0, next_num_tokens)

        return next_num_tokens

    def _get_seq_priority(self, seq: Sequence) -> Any:
        return (seq.arrival_time, seq.seq_id)
