from abc import abstractmethod
from collections import OrderedDict, defaultdict
from itertools import chain
from math import ceil
from typing import Any, Dict, List, Optional

from vajra.config import BaseSchedulerConfig, CacheConfig, ModelConfig, ParallelConfig
from vajra.core.block_space_manager import BlockSpaceManager
from vajra.datatypes import (
    SchedulerOutput,
    Sequence,
    SequenceScheduleMetadata,
    SequenceStatus,
)
from vajra.logger import init_logger
from vajra.metrics.metrics_store import MetricsStore
from vajra.utils.threading_utils import synchronized

logger = init_logger(__name__)

MAX_NUM_SKIPPED_SEQS = 10
ALLOCATION_MAX_TOKEN_THRESHOLD = 500


class BatchFormationTracker:
    def __init__(
        self,
        schedule_id: int,
        max_micro_batch_size: int,
        kv_parallel_size: int,
        max_num_tokens_per_kvp_group: int,
    ):
        self.schedule_id: int = schedule_id
        self.max_micro_batch_size: int = max_micro_batch_size
        self.kv_parallel_size: int = kv_parallel_size
        self.max_num_tokens_per_kvp_group: int = max_num_tokens_per_kvp_group

        self.num_sequences: int = 0
        self.sequences: List[Sequence] = []
        self.ignored_sequence_ids: List[str] = []
        self.preempted_sequence_ids: List[str] = []

        self.per_kvp_group_sequences: List[List[Sequence]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_num_q_tokens: List[List[int]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_num_kv_tokens: List[List[int]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_num_active_kvp_groups: List[List[int]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_last_kvp_group_ids: List[List[int]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_seq_num_processed_tokens: List[List[int]] = [
            [] for _ in range(self.kv_parallel_size)
        ]
        self.per_kvp_group_total_num_q_tokens: List[int] = [
            0 for _ in range(self.kv_parallel_size)
        ]

        self.batch_num_q_tokens: List[int] = []
        self.batch_group_mapping: List[Dict[int, int]] = []
        self.batch_active_group_ids: List[List[int]] = []

    def _get_num_kv_tokens(
        self,
        num_processed_tokens: int,
        active_kvp_group_ids: List[int],
        is_last_group: bool,
    ) -> int:
        if is_last_group:
            num_kv_tokens_in_other_groups = (
                len(active_kvp_group_ids) - 1
            ) * self.max_num_tokens_per_kvp_group
            num_kv_tokens = num_processed_tokens - num_kv_tokens_in_other_groups
        else:
            num_kv_tokens = self.max_num_tokens_per_kvp_group
        assert num_kv_tokens >= 0
        return num_kv_tokens

    def add_sequence(
        self,
        seq: Sequence,
        num_q_tokens: int,
        active_kvp_group_ids: List[int],
        kvp_group_block_counter: Dict[int, int],
    ) -> None:
        self.num_sequences += 1

        self.sequences.append(seq)
        self.batch_num_q_tokens.append(num_q_tokens)
        self.batch_group_mapping.append(kvp_group_block_counter)
        self.batch_active_group_ids.append(active_kvp_group_ids)

        num_processed_tokens = seq.get_num_tokens_stage_processed()

        for i, kvp_group_id in enumerate(active_kvp_group_ids):
            is_last_group = i == len(active_kvp_group_ids) - 1
            num_kv_tokens = self._get_num_kv_tokens(
                num_processed_tokens, active_kvp_group_ids, is_last_group
            )

            self.per_kvp_group_sequences[kvp_group_id].append(seq)
            self.per_kvp_group_num_q_tokens[kvp_group_id].append(num_q_tokens)
            self.per_kvp_group_num_kv_tokens[kvp_group_id].append(num_kv_tokens)
            self.per_kvp_group_num_active_kvp_groups[kvp_group_id].append(
                len(active_kvp_group_ids)
            )
            self.per_kvp_group_seq_num_processed_tokens[kvp_group_id].append(
                num_processed_tokens
            )
            self.per_kvp_group_last_kvp_group_ids[kvp_group_id].append(
                active_kvp_group_ids[-1]
            )
            self.per_kvp_group_total_num_q_tokens[kvp_group_id] += num_q_tokens

    def add_ignored_sequence(self, seq: Sequence) -> None:
        self.ignored_sequence_ids.append(seq.seq_id)

    def add_preempted_sequence(self, seq: Sequence) -> None:
        self.preempted_sequence_ids.append(seq.seq_id)

    def can_add_sequences(self) -> bool:
        return self.num_sequences < self.max_micro_batch_size

    def get_q_tokens_for_kvp_groups(self, active_kvp_group_ids: List[int]) -> List[int]:
        return [
            self.per_kvp_group_total_num_q_tokens[kvp_group_id]
            for kvp_group_id in active_kvp_group_ids
        ]

    def get_batch(self) -> SchedulerOutput:
        seq_schedule_metadata_list: List[SequenceScheduleMetadata] = []

        for i, seq in enumerate(self.sequences):
            seq_schedule_metadata_list.append(
                SequenceScheduleMetadata(
                    schedule_id=self.schedule_id,
                    seq_id=seq.seq_id,
                    num_q_tokens=self.batch_num_q_tokens[i],
                    kvp_group_block_counter=self.batch_group_mapping[i],
                    kvp_group_ids=self.batch_active_group_ids[i],
                )
            )

        return SchedulerOutput(
            id=self.schedule_id,
            ignored_seq_ids=self.ignored_sequence_ids,
            preempted_seq_ids=self.preempted_sequence_ids,
            seq_schedule_metadata_list=seq_schedule_metadata_list,
        )


class BaseScheduler:
    def __init__(
        self,
        model_config: ModelConfig,
        scheduler_config: BaseSchedulerConfig,
        cache_config: CacheConfig,
        parallel_config: ParallelConfig,
    ) -> None:
        self.metrics_store = MetricsStore.get_instance()
        self.model_config = model_config
        self.scheduler_config = scheduler_config
        self.cache_config = cache_config
        self.parallel_config = parallel_config

        self.kvp_size = parallel_config.kv_parallel_size

        if self.kvp_size == 1:
            self.max_num_tokens_per_kvp_group = model_config.max_model_len
        else:
            assert parallel_config.max_num_tokens_per_kvp_group is not None
            assert (
                parallel_config.max_num_tokens_per_kvp_group > cache_config.block_size
            )
            assert (
                parallel_config.max_num_tokens_per_kvp_group % cache_config.block_size
                == 0
            )
            self.max_num_tokens_per_kvp_group = (
                parallel_config.max_num_tokens_per_kvp_group
            )

        self.max_num_blocks_per_kvp_group = ceil(
            self.max_num_tokens_per_kvp_group / cache_config.block_size
        )
        self.max_num_blocks_per_kvp_group = min(
            self.max_num_blocks_per_kvp_group, cache_config.num_gpu_blocks
        )

        self.max_seq_len = (
            self.kvp_size * self.max_num_blocks_per_kvp_group * cache_config.block_size
        )

        # we maintain this just for logging purposes
        self._iteration_id = -1

        self.block_managers_map: Dict[int, BlockSpaceManager] = {}
        for i in range(self.kvp_size):
            self.block_managers_map[i] = BlockSpaceManager(
                cache_config.block_size,
                cache_config.num_gpu_blocks,
                model_config.max_model_len,
            )

        self.seq_kvp_group_block_counter: Dict[str, OrderedDict[int, int]] = (
            defaultdict(OrderedDict)
        )
        self.seq_block_counter: Dict[str, int] = defaultdict(int)
        self.kvp_group_pending_prefill_work: List[int] = [
            0 for _ in range(self.kvp_size)
        ]

        self.prompt_limit = model_config.max_model_len

        # number of running batches should be less than or equal to the number of pipeline stages
        self.num_running_batches = 0
        self.num_running_stages = 0

        # Sequence groups in the WAITING state.
        self.waiting: List[Sequence] = []
        # Sequence groups in the RUNNING state.
        self.running: List[Sequence] = []

        self.last_batch_execution_time: Optional[float] = None

    def reset_state(self) -> None:
        self._iteration_id = -1
        self.last_batch_execution_time = None

    def _get_batch_formation_tracker(self) -> BatchFormationTracker:
        return BatchFormationTracker(
            schedule_id=self._iteration_id,
            max_micro_batch_size=self.scheduler_config.max_batch_size,
            kv_parallel_size=self.kvp_size,
            max_num_tokens_per_kvp_group=self.max_num_tokens_per_kvp_group,
        )

    @synchronized
    def add_seq(self, seq: Sequence) -> None:
        # Add sequence groups to the waiting queue.
        self.waiting.append((self._get_seq_priority(seq), seq))

    def has_unfinished_seqs(self) -> bool:
        return self.waiting or self.running

    def get_num_unfinished_seqs(self) -> int:
        return len(self.waiting) + len(self.running)

    @abstractmethod
    def _get_seq_priority(self, seq: Sequence) -> Any:
        pass

    def _sort_waiting_queue(self) -> None:
        self.waiting.sort(key=lambda x: x[0])

    def _get_allocation_order(self, kvp_group_ids: List[int]) -> List[int]:
        """
        We are simply picking the kvp group with the least prefill work.
        We use the square of number of prefill tokens as a simple proxy for prefill work of now.

        TODO(amey): since the initial chunks are linearly proportional to the number of tokens,
        this can lead to some imbalance in the allocation. We can improve this in the future.
        """
        return sorted(
            kvp_group_ids,
            key=lambda kvp_group_id: self.kvp_group_pending_prefill_work[kvp_group_id],
        )

    def _preempt(
        self,
        seq: Sequence,
    ) -> None:
        assert seq.is_executing()
        self._free_seq(seq)
        self.add_seq(seq)

    def _allocate(
        self, seq: Sequence, batch_formation_tracker: BatchFormationTracker
    ) -> bool:
        """
        We use a naive approach to allocate memory where we allocate all the memory
        required by the seq in one go. This is because we expect the compute requirement
        to far exceed the memory requirement. In KVP, incremental memory allocation can
        lead to deadlocks -- where multiple long seqs are waiting for memory to be available
        on a new kvp group, but none of them can proceed because the memory is not available.

        TODO(amey): This is a naive approach and can be improved in the future. Especially, offloading
        memory allocation to CPU can be a good solution, especially for longer seqs.

        While allocating memory, we must choose the kvp groups such that we have minimal
        compute contention. While also ensuring that we don't create memory hotspots.
        The allocate method offloads this responsibility to _get_allocation_order method.
        """

        # if seq is already allocated, return
        if seq.seq_id in self.seq_block_counter:
            return True

        num_blocks = len(seq.logical_token_blocks)

        # if seq is too large, ignore it
        if num_blocks > self.kvp_size * self.max_num_blocks_per_kvp_group:
            logger.warning(
                f"Ignoring seq_id: {seq.seq_id} due to max num blocks per kvp group limit."
            )
            return False

        # filter the busy kvp groups based on the num q tokens
        free_kvp_group_ids = [
            kvp_group_id
            for kvp_group_id in range(self.kvp_size)
            if batch_formation_tracker.per_kvp_group_total_num_q_tokens[kvp_group_id]
            < ALLOCATION_MAX_TOKEN_THRESHOLD
        ]

        if not free_kvp_group_ids:
            return False

        # if seq fits in one kvp group, allocate it to first available kvp group
        if num_blocks < self.max_num_blocks_per_kvp_group:
            for kvp_group_id in self._get_allocation_order(free_kvp_group_ids):
                if self.block_managers_map[kvp_group_id].can_allocate_blocks(
                    num_blocks
                ):
                    self.block_managers_map[kvp_group_id].allocate(seq, num_blocks)
                    self.seq_kvp_group_block_counter[seq.seq_id][
                        kvp_group_id
                    ] = num_blocks
                    self.seq_block_counter[seq.seq_id] = num_blocks
                    return True
            return False

        num_kv_parallel_groups = ceil(num_blocks / self.max_num_blocks_per_kvp_group)
        last_group_num_blocks = num_blocks - self.max_num_blocks_per_kvp_group * (
            num_kv_parallel_groups - 1
        )

        num_groups_found = 0
        last_group_found = False
        kvp_group_ids: List[int] = []
        last_kvp_group_id: Optional[int] = None

        for kvp_group_id in self._get_allocation_order(free_kvp_group_ids):
            block_manager = self.block_managers_map[kvp_group_id]
            if block_manager.can_allocate_blocks(self.max_num_blocks_per_kvp_group):
                num_groups_found += 1
                kvp_group_ids.append(kvp_group_id)
            elif (
                last_group_num_blocks
                and not last_group_found
                and block_manager.can_allocate_blocks(last_group_num_blocks)
            ):
                last_group_found = True
                num_groups_found += 1
                last_kvp_group_id = kvp_group_id
            if num_groups_found == num_kv_parallel_groups:
                break

        if num_groups_found != num_kv_parallel_groups:
            return False

        if last_kvp_group_id:
            kvp_group_ids.append(last_kvp_group_id)
        else:
            last_kvp_group_id = kvp_group_ids[-1]

        for kvp_group_id in kvp_group_ids:
            if kvp_group_id == last_kvp_group_id:
                self.block_managers_map[kvp_group_id].allocate(
                    seq, last_group_num_blocks
                )
                self.seq_kvp_group_block_counter[seq.seq_id][
                    kvp_group_id
                ] = last_group_num_blocks
            else:
                self.block_managers_map[kvp_group_id].allocate(
                    seq, self.max_num_blocks_per_kvp_group
                )
                self.seq_kvp_group_block_counter[seq.seq_id][
                    kvp_group_id
                ] = self.max_num_blocks_per_kvp_group

            self.kvp_group_pending_prefill_work[kvp_group_id] += seq.prompt_len**2

        self.seq_block_counter[seq.seq_id] = num_blocks
        return True

    def _free_seq(self, seq: Sequence) -> None:
        for kvp_group_id in self.seq_kvp_group_block_counter[seq.seq_id]:
            self.block_managers_map[kvp_group_id].free(seq)
        del self.seq_kvp_group_block_counter[seq.seq_id]
        del self.seq_block_counter[seq.seq_id]

    def _get_last_kv_group_id(self, seq: Sequence) -> int:
        return next(reversed(self.seq_kvp_group_block_counter[seq.seq_id]))

    def _can_append_slot(self, seq: Sequence) -> bool:
        last_kvp_group_id = self._get_last_kv_group_id(seq)
        return self.block_managers_map[last_kvp_group_id].can_append_slot()

    def _append_slot(self, seq: Sequence) -> None:
        last_kvp_group_id = self._get_last_kv_group_id(seq)
        num_total_blocks = self.seq_block_counter[seq.seq_id]
        has_appended = self.block_managers_map[last_kvp_group_id].append_slot(
            seq, num_total_blocks
        )
        self.seq_kvp_group_block_counter[seq.seq_id][last_kvp_group_id] += int(
            has_appended
        )
        self.seq_block_counter[seq.seq_id] += int(has_appended)

    def _get_active_kvp_group_ids(self, seq: Sequence) -> List[int]:
        kvp_group_ids = list(self.seq_kvp_group_block_counter[seq.seq_id])

        if seq.prompt_processing_finished:
            return kvp_group_ids

        num_processed_tokens = seq.get_num_tokens_stage_processed()
        num_groups = num_processed_tokens // self.max_num_tokens_per_kvp_group + 1
        return kvp_group_ids[:num_groups]

    @abstractmethod
    def _get_seq_next_num_q_tokens(
        self, seq: Sequence, batch_formation_tracker: BatchFormationTracker
    ) -> int:
        pass

    def _check_seq_prompt_length(self, seq: Sequence) -> bool:
        return seq.prompt_len <= self.max_seq_len

    def _ensure_can_append_slot(
        self, seq: Sequence, batch_formation_tracker: BatchFormationTracker
    ) -> bool:
        if self._can_append_slot(seq):
            return True

        could_ensure_memory = False

        last_kvp_group_id = self._get_last_kv_group_id(seq)

        # Find the last seq that contains allocation on the last kv group
        # TODO(amey): here we are just restarting the seq based on the scheduling preference order
        # however, this doesn't account for the size of the seq -- so potentially we could be
        # restarting a large seq instead of a smaller one. We can improve this in the future.
        for i, seq in enumerate(chain(reversed(self.waiting), reversed(self.running))):
            if not last_kvp_group_id in self.seq_kvp_group_block_counter[seq.id]:
                continue

            if i < len(self.waiting):
                # We're in the waiting list
                self.waiting.pop(-1 * (len(self.waiting) - i))
            else:
                # We're in the running list, adjust index relative to running list
                running_index = i - len(self.waiting)
                self.running.pop(-1 * (len(self.running) - running_index))

            self._preempt(seq)
            batch_formation_tracker.add_preempted_sequence(seq.id)
            could_ensure_memory = True
            break

        if not could_ensure_memory:
            self._preempt(seq)
            batch_formation_tracker.add_preempted_sequence(seq)

        return could_ensure_memory

    def on_stage_completed(self, seqs: List[Sequence]) -> None:
        self.num_running_stages -= 1

        for seq in seqs:
            assert not seq.is_finished()

            if not seq.is_paused():
                continue

            assert not seq.prompt_stage_processing_finished, "Unreachable state."
            self.add_seq(seq)

    def on_step_completed(self, seqs: List[Sequence], execution_time: float) -> None:
        self.num_running_batches -= 1
        if not self.parallel_config.pipeline_parallel_size > 1:
            self.num_running_stages -= 1

        self.last_batch_execution_time = execution_time

        for seq in seqs:
            if seq.is_finished():
                self._free_seq(seq)
                continue

            if not seq.is_paused():
                continue

            if seq.prompt_processing_finished:
                self.running.append(seq)
            elif not self.parallel_config.enable_sequence_pipeline_parallel:
                # TODO(Amey): Rethink the running/paused transitions split between seq manager & scheduler
                self.add_seq(seq)

    def _check_seq_prompt_length(self, seq: Sequence) -> bool:
        if len(seq) > self.prompt_limit:
            logger.warning(
                f"Input prompt ({len(seq)} tokens) is too long"
                f" and exceeds limit of {self.prompt_limit}"
            )
            seq.status = SequenceStatus.FINISHED_IGNORED
            self.waiting.pop(0)
            return False

        return True

    @synchronized
    def _schedule(self) -> SchedulerOutput:
        batch_formation_tracker = self._get_batch_formation_tracker()

        while self.running:
            seq = self.running[0]

            assert not seq.is_finished()
            assert seq.prompt_stage_processing_finished
            assert seq.is_paused()

            if not batch_formation_tracker.can_add_sequences():
                break

            self.running.pop(0)

            if not self._ensure_can_append_slot(seq, batch_formation_tracker):
                continue

            self._append_slot(seq)
            active_kvp_group_ids = self._get_active_kvp_group_ids(seq)

            batch_formation_tracker.add_sequence(
                seq,
                1,
                active_kvp_group_ids,
                self.seq_kvp_group_block_counter[seq.seq_id],
            )

        self._sort_waiting_queue()

        num_skipped_seqs = 0

        while (
            len(self.waiting) > num_skipped_seqs
            and num_skipped_seqs < MAX_NUM_SKIPPED_SEQS
        ):
            _, seq = self.waiting[num_skipped_seqs]

            if not self._check_seq_prompt_length(seq):
                self.waiting.pop(num_skipped_seqs)
                batch_formation_tracker.add_ignored_sequence(seq)
                logger.warning(
                    f"Ignoring seq_id: {seq.seq_id} due to max seq length limit."
                )
                continue

            if not batch_formation_tracker.can_add_sequences():
                break

            assert not seq.prompt_stage_processing_finished
            assert not seq.is_finished()

            assert (
                seq.is_paused() or seq.is_waiting_preempted() or seq.is_waiting()
            ), f"seq_id: {seq.seq_id}, status: {seq.status}"

            if not self._allocate(seq, batch_formation_tracker):
                num_skipped_seqs += 1
                continue

            active_kvp_group_ids = self._get_active_kvp_group_ids(seq)
            num_q_tokens = self._get_seq_next_num_q_tokens(seq, batch_formation_tracker)

            if num_q_tokens == 0:
                num_skipped_seqs += 1
                continue

            num_processed_tokens = seq.get_num_tokens_stage_processed()
            work_delta = (
                num_processed_tokens + num_q_tokens
            ) ** 2 - num_processed_tokens**2

            for kvp_group_id in active_kvp_group_ids:
                self.kvp_group_pending_prefill_work[kvp_group_id] -= work_delta

            self.waiting.pop(num_skipped_seqs)

            batch_formation_tracker.add_sequence(
                seq,
                num_q_tokens,
                active_kvp_group_ids,
                self.seq_kvp_group_block_counter[seq.seq_id],
            )

        batch = batch_formation_tracker.get_batch()

        return batch

    def schedule(self) -> SchedulerOutput:
        # Schedule sequence groups.
        # This function call changes the internal states of the scheduler
        # such as self.running and self.waiting.
        self._iteration_id += 1

        if (
            self.num_running_batches >= self.parallel_config.pipeline_parallel_size
            or self.num_running_stages != 0
        ):
            return SchedulerOutput(
                self._iteration_id,
                ignored_seq_ids=[],
                preempted_seq_ids=[],
                seq_schedule_metadata_list=[],
            )

        scheduler_output = self._schedule()

        if not scheduler_output.is_empty:
            self.num_running_batches += 1
            self.num_running_stages += 1

        return scheduler_output

    def free_finished_seqs(self) -> None:
        for seq in self.running:
            if seq.is_finished():
                self._free_seq(seq)
        self.running = [seq for seq in self.running if not seq.is_finished()]
