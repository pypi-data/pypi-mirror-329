"""Sequence class."""

from typing import List, Optional

from .block import LogicalTokenBlock
from .sampling_params import SamplingParams
from .sequence_state import SequenceState
from .sequence_status import SequenceStatus


class Sequence:
    """Stores the data, status, and block information of a sequence.

    Args:
        seq_id: The ID of the sequence.
        prompt: The prompt of the sequence.
        prompt_token_ids: The token IDs of the prompt.
        block_size: The block size of the sequence. Should be the same as the
            block size used by the block manager and cache engine.
    """

    def __init__(
        self,
        seq_id: str,
        prompt: str,
        prompt_token_ids: List[int],
        block_size: int,
        eos_token_id: int,
        arrival_time: float,
        sampling_params: SamplingParams,
    ) -> None:
        self.seq_id = seq_id
        self.prompt = prompt
        self.block_size = block_size
        self.eos_token_id = eos_token_id
        self.arrival_time = arrival_time
        self.sampling_params = sampling_params
        self.prompt_token_ids = prompt_token_ids

        self.output_token_ids: List[int] = []
        self.prompt_tokens_processed = 0
        self.prompt_tokens_stage_processed = 0
        self.prompt_processing_finished = False
        self.prompt_stage_processing_finished = False

        self.output_text = ""

        self.logical_token_blocks: List[LogicalTokenBlock] = []
        # Initialize the logical token blocks with the prompt token ids.
        self._append_tokens_to_blocks(prompt_token_ids)

        # Used for incremental detokenization
        self.prefix_offset = 0
        self.read_offset = 0
        # TODO(amey): Clean up this code
        # Input + output tokens -- required only for incremental decoding
        self.tokens: Optional[List[str]] = None

        self.state = SequenceState(seq_id, arrival_time, len(prompt_token_ids))

    @property
    def status(self) -> SequenceStatus:
        return self.state.status

    @status.setter
    def status(self, status: SequenceStatus) -> None:
        self.state.status = status

    def _append_logical_block(self) -> None:
        block = LogicalTokenBlock(
            block_number=len(self.logical_token_blocks),
            block_size=self.block_size,
        )
        self.logical_token_blocks.append(block)

    def _append_tokens_to_blocks(self, token_ids: List[int]) -> None:
        cursor = 0
        while cursor < len(token_ids):
            if not self.logical_token_blocks:
                self._append_logical_block()

            last_block = self.logical_token_blocks[-1]
            if last_block.is_full:
                self._append_logical_block()
                last_block = self.logical_token_blocks[-1]

            num_empty_slots = last_block.num_empty_slots
            last_block.append_tokens(token_ids[cursor : cursor + num_empty_slots])
            cursor += num_empty_slots

    def update_prompt_tokens_processed(self, num_tokens: int) -> None:
        assert not self.prompt_processing_finished
        assert num_tokens > 0

        self.prompt_tokens_processed += num_tokens
        assert self.prompt_tokens_processed <= len(self.prompt_token_ids)

        if self.prompt_tokens_processed == len(self.prompt_token_ids):
            assert self.prompt_stage_processing_finished
            self.prompt_processing_finished = True
            self.state.on_prompt_processing_completed()

    def update_prompt_tokens_stage_processed(self, num_tokens: int) -> None:
        assert not self.prompt_processing_finished
        assert not self.prompt_stage_processing_finished
        assert num_tokens > 0, (
            f"Number of tokens processed should be greater than 0. "
            f"Got {num_tokens}, prompt_tokens_stage_processed: {self.prompt_tokens_stage_processed}"
            f"prompt len: {len(self.prompt_token_ids)}"
        )
        self.prompt_tokens_stage_processed += num_tokens
        assert self.prompt_tokens_stage_processed <= len(self.prompt_token_ids)
        if self.prompt_tokens_stage_processed == len(self.prompt_token_ids):
            self.prompt_stage_processing_finished = True

    def append_token_id(
        self,
        token_id: int,
    ) -> None:
        # the token need not be appended to the sequence
        # when processing partial prefill chunks
        assert self.prompt_processing_finished

        self.output_token_ids.append(token_id)
        self._append_tokens_to_blocks([token_id])
        self.state.on_token_generated()

    def __len__(self) -> int:
        return len(self.output_token_ids) + len(self.prompt_token_ids)

    @property
    def prompt_len(self) -> int:
        return len(self.prompt_token_ids)

    @property
    def output_len(self) -> int:
        return len(self.output_token_ids)

    def get_num_prompt_tokens_processed(self) -> int:
        return self.prompt_tokens_processed

    def get_num_prompt_tokens_stage_processed(self) -> int:
        return self.prompt_tokens_stage_processed

    def get_num_tokens_stage_processed(self) -> int:
        return self.prompt_tokens_stage_processed + len(self.output_token_ids)

    def get_num_tokens_processed(self) -> int:
        return self.prompt_tokens_processed + len(self.output_token_ids)

    def get_last_token_id(self) -> int:
        if not self.output_token_ids:
            return self.prompt_token_ids[-1]
        return self.output_token_ids[-1]

    def get_last_n_token_ids(self, n: int) -> List[int]:
        assert n <= len(self.prompt_token_ids) + len(self.output_token_ids)

        if n <= len(self.output_token_ids):
            return self.output_token_ids[-n:]

        num_prompt_tokens = n - len(self.output_token_ids)
        return self.prompt_token_ids[-num_prompt_tokens:] + self.output_token_ids

    def is_finished(self) -> bool:
        return SequenceStatus.is_finished(self.status)

    def is_executing(self) -> bool:
        return SequenceStatus.is_executing(self.status)

    def is_waiting(self) -> bool:
        return SequenceStatus.is_waiting(self.status)

    def is_paused(self) -> bool:
        return SequenceStatus.is_paused(self.status)

    def is_running(self) -> bool:
        return SequenceStatus.is_running(self.status)

    def is_waiting_preempted(self) -> bool:
        return SequenceStatus.is_waiting_preempted(self.status)

    def reset(self, force_reset_state: bool = False) -> None:
        if force_reset_state:
            self.state = SequenceState(
                self.seq_id, self.arrival_time, len(self.prompt_token_ids)
            )
        else:
            self.status = SequenceStatus.WAITING_PREEMPTED
        self.prompt_tokens_processed = 0
        self.prompt_tokens_stage_processed = 0
        self.prompt_processing_finished = False
        self.prompt_stage_processing_finished = False
        self.prompt_token_ids = self.prompt_token_ids + self.output_token_ids
        self.output_token_ids = []

    def reset_for_recompute(self):
        self.reset()

    def reset_for_worker(self):
        self.reset(force_reset_state=True)

    def check_stop(self, num_new_tokens: int) -> None:
        """Stop the finished sequences."""
        # TODO: add back stop string support

        # Check if the sequence has reached max_tokens.
        if self.output_len == self.sampling_params.max_tokens:
            self.status = SequenceStatus.FINISHED_LENGTH_CAPPED
            return

        # Check if the sequence has generated the EOS token.
        if (not self.sampling_params.ignore_eos) and any(
            [
                token_id == self.eos_token_id
                for token_id in self.get_last_n_token_ids(num_new_tokens)
            ]
        ):
            self.status = SequenceStatus.FINISHED_STOPPED
            return

    def __repr__(self) -> str:
        return (
            f"Sequence(seq_id={self.seq_id}, "
            f"status={self.status.name}, "
            f"num_blocks={len(self.logical_token_blocks)}, "
            f"num_prompt_tokens={len(self.prompt_token_ids)}, "
            f"num_output_tokens={len(self.output_token_ids)}, "
            f"prompt_processing_finished={self.prompt_processing_finished}, "
            f"num_prompt_tokens_processed={self.prompt_tokens_processed}, "
            f"num_prompt_tokens_stage_processed={self.prompt_tokens_stage_processed}, "
            f"prompt_stage_processing_finished={self.prompt_stage_processing_finished})"
        )
