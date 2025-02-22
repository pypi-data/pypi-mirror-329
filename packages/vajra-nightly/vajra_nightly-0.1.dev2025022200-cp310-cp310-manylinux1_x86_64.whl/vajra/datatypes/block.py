"""Token blocks."""

from typing import List

_BLANK_TOKEN_ID = -1


class LogicalTokenBlock:
    """A block that stores a contiguous chunk of tokens from left to right.

    Logical blocks are used to represent the states of the corresponding
    physical blocks in the KV cache.
    """

    def __init__(
        self,
        block_number: int,
        block_size: int,
    ) -> None:
        self.block_number = block_number
        self.block_size = block_size

        self.token_ids = [_BLANK_TOKEN_ID] * block_size
        self.num_tokens = 0

    @property
    def is_empty(self) -> bool:
        return self.num_tokens == 0

    @property
    def num_empty_slots(self) -> int:
        return self.block_size - self.num_tokens

    @property
    def is_full(self) -> bool:
        return self.num_tokens == self.block_size

    def append_tokens(self, token_ids: List[int]) -> None:
        assert len(token_ids) <= self.num_empty_slots
        curr_idx = self.num_tokens
        self.token_ids[curr_idx : curr_idx + len(token_ids)] = token_ids
        self.num_tokens += len(token_ids)

    def get_last_token_id(self) -> int:
        assert self.num_tokens > 0
        return self.token_ids[self.num_tokens - 1]
