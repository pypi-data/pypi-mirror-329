from typing import List, Optional, Tuple

import torch
import torch.distributed

from vajra._native.datatypes import SequenceMetadata
from vajra.config import SystemConfig
from vajra.datatypes import SamplerOutputs, SamplingParams, Sequence
from vajra.logger import init_logger
from vajra.metrics.constants import CpuOperationMetrics
from vajra.metrics.cpu_timer import CpuTimer
from vajra.model_executor import get_model, set_random_seed
from vajra.model_executor.layers.attention.attention_wrapper import AttentionWrapper
from vajra.model_executor.layers.sampler import Sampler
from vajra.model_executor.parallel_utils import (
    recv_from_last_pipeline_stage,
    send_to_next_pipeline_stage,
)
from vajra.model_executor.parallel_utils.parallel_state import (
    is_pipeline_first_stage,
    is_pipeline_last_stage,
)
from vajra.model_executor.utils import pad_to_alignment
from vajra.utils import get_gpu_memory
from vajra.worker.cache_engine import CacheEngine

logger = init_logger(__name__)


class ModelRunner:

    def __init__(
        self,
        config: SystemConfig,
        device: torch.device,
        rank: int,
    ):
        self.config = config
        self.device = device
        self.rank = rank

        AttentionWrapper.create_instance(
            config.model_config,
            config.parallel_config,
            config.worker_config,
            config.cache_config.block_size,
            self.device,
        )
        self.model = get_model(config)

        self.sampler: Optional[Sampler] = None
        if self.model.lm_head:
            self.sampler = Sampler(
                self.model.lm_head.weight, self.model.config.vocab_size
            )

        self.is_pipeline_first_stage = is_pipeline_first_stage()
        self.is_pipeline_last_stage = is_pipeline_last_stage()

        self._prepare_inputs_timer = CpuTimer(
            CpuOperationMetrics.PREPARE_INPUTS, rank=self.rank
        )
        self._sampler_timer = CpuTimer(CpuOperationMetrics.SAMPLER, rank=self.rank)
        self._model_execution_timer = CpuTimer(
            CpuOperationMetrics.MODEL_EXECUTION, rank=self.rank
        )
        self._attn_begin_forward_timer = CpuTimer(
            CpuOperationMetrics.ATTN_BEGIN_FORWARD, rank=self.rank
        )

    def _prepare_inputs(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        input_tokens: List[int] = []
        input_positions: List[int] = []

        for seq, seq_metadata in zip(seqs, seq_metadata_list):
            num_q_tokens = seq_metadata.num_q_tokens
            input_tokens.extend(seq.get_last_n_token_ids(num_q_tokens))

            start_position = seq.get_num_tokens_stage_processed()
            end_position = start_position + num_q_tokens
            input_positions.extend(range(start_position, end_position))

        # Optimization: Pad the input length to be a multiple of 8.
        # This is required for utilizing the Tensor Cores in NVIDIA GPUs.
        input_tokens = pad_to_alignment(input_tokens, multiple_of=8)
        input_positions = pad_to_alignment(input_positions, multiple_of=8)

        # Convert to tensors.
        tokens_tensor = torch.tensor(input_tokens, dtype=torch.long, device=self.device)
        positions_tensor = torch.tensor(
            input_positions, dtype=torch.long, device=self.device
        )

        return tokens_tensor, positions_tensor

    @torch.inference_mode()
    def profile_num_available_blocks(
        self,
        block_size: int,
        gpu_memory_utilization: float,
    ) -> int:
        torch.cuda.set_device(self.device)

        # Profile the memory usage of the model and get the maximum number of
        # cache blocks that can be allocated with the remaining free memory.
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

        # Enable top-k sampling to reflect the accurate memory usage.
        vocab_size = self.model.config.vocab_size
        sampling_params = SamplingParams(top_p=0.99, top_k=vocab_size - 1)

        seqs: List[Sequence] = []
        seq_metadata_list: List[SequenceMetadata] = []

        # Profile memory usage with a single `chunk_size` chunk
        # which is the last chunk in the longest supported sequence.
        seq_len = int(self.config.model_config.max_model_len)

        chunk_size = int(
            min(self.config.scheduler_config.get_max_num_batched_tokens(), seq_len)
        )

        seq = Sequence(
            seq_id=str(0),
            prompt="",
            prompt_token_ids=[0] * seq_len,
            block_size=block_size,
            eos_token_id=1,
            arrival_time=0.0,
            sampling_params=sampling_params,
        )
        seq_metadata = SequenceMetadata(
            schedule_id=0,
            seq_id=seq.seq_id,
            num_q_tokens=chunk_size,
            num_kv_tokens=seq_len,
            block_table=[],
            kvp_group_ids=[],
            save_kv_cache=True,
        )
        seqs.append(seq)
        seq_metadata_list.append(seq_metadata)

        input_tokens, input_positions = self._prepare_inputs(seqs, seq_metadata_list)
        AttentionWrapper.get_instance().begin_forward(seq_metadata_list)

        if not self.is_pipeline_first_stage:
            # hidden_states_shape: num_tokens x hidden_size
            input_tokens = torch.empty(
                (input_positions.shape[0], self.model.config.hidden_size),
                dtype=self.model.config.dtype,
                device=self.device,
            )

        # Execute the model.
        num_layers = self.config.model_config.get_num_layers(
            self.config.parallel_config
        )
        self.model(
            hidden_states=input_tokens,
            positions=input_positions,
            kv_caches=[torch.empty(1)] * num_layers,
        )

        # Calculate the number of blocks that can be allocated with the
        # profiled peak memory.
        torch.cuda.synchronize()
        peak_memory = torch.cuda.max_memory_allocated()
        total_gpu_memory = get_gpu_memory()
        logger.info(
            f"Completed profiling, peak_memory: {peak_memory}, total_gpu_memory: {total_gpu_memory}, gpu_memory_utilization: {gpu_memory_utilization}, block_size: {block_size}"
        )
        cache_block_size = CacheEngine.get_cache_block_size(
            block_size, self.config.model_config, self.config.parallel_config
        )
        num_gpu_blocks = int(
            (total_gpu_memory * gpu_memory_utilization - peak_memory)
            // cache_block_size
        )
        num_gpu_blocks = max(num_gpu_blocks, 0)
        torch.cuda.empty_cache()

        AttentionWrapper.get_instance().end_forward()

        # Reset the seed to ensure that the random state is not affected by
        # the model initialization and profiling.
        set_random_seed(self.config.model_config.seed)
        return num_gpu_blocks

    def run(
        self,
        seqs: List[Sequence],
        seq_metadata_list: List[SequenceMetadata],
        gpu_cache: Optional[List[torch.Tensor]] = None,
    ) -> Optional[SamplerOutputs]:
        if not seq_metadata_list:
            return []

        # Prepare input tensors.
        with self._prepare_inputs_timer:
            input_tokens, input_positions = self._prepare_inputs(
                seqs, seq_metadata_list
            )

        if not self.is_pipeline_first_stage:
            # hidden_states_shape: num_tokens x hidden_size
            input_tokens = torch.empty(
                (input_positions.shape[0], self.model.config.hidden_size),
                dtype=self.model.config.dtype,
                device=self.device,
            )
            input_tokens = recv_from_last_pipeline_stage(
                input_tokens, self.config.parallel_config.enable_pipeline_tp_comm_opt
            )

        with self._attn_begin_forward_timer:
            AttentionWrapper.get_instance().begin_forward(seq_metadata_list)

        torch.cuda.synchronize()

        with self._model_execution_timer:
            output = self.model(
                input_tokens,
                input_positions,
                gpu_cache,
            )
        torch.cuda.synchronize()

        AttentionWrapper.get_instance().end_forward()

        if self.sampler is not None:
            with self._sampler_timer:
                output = self.sampler(output, seqs, seq_metadata_list)
        else:  # is not last stage
            assert not self.is_pipeline_last_stage
            send_to_next_pipeline_stage(
                output, self.config.parallel_config.enable_pipeline_tp_comm_opt
            )

        return output
