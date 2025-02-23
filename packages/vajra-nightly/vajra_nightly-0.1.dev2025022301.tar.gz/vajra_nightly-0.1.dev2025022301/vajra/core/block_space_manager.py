"""A block manager that manages token blocks."""

from typing import Dict, List

from vajra.datatypes import Sequence


class BlockAllocator:
    """Manages free physical token blocks for a device.

    The allocator maintains a list of free blocks and allocates a block when
    requested. When a block is freed, its reference count is decremented. If
    the reference count becomes zero, the block is added back to the free list.
    """

    def __init__(
        self,
        block_size: int,
        num_blocks: int,
    ) -> None:
        self.block_size = block_size
        self.num_blocks = num_blocks

        # Initialize the free blocks.
        self.free_blocks: List[int] = []
        for block_id in range(num_blocks):
            self.free_blocks.append(block_id)

    def allocate(self) -> int:
        if not self.free_blocks:
            raise ValueError("Out of memory! No free blocks are available.")
        block = self.free_blocks.pop()
        return block

    def free(self, block_id: int) -> None:
        self.free_blocks.append(block_id)

    def get_num_free_blocks(self) -> int:
        return len(self.free_blocks)


# Mapping: logical block number -> physical block id.
BlockTable = List[int]


class BlockSpaceManager:
    """Manages the mapping between logical and physical token blocks."""

    def __init__(
        self,
        block_size: int,
        num_gpu_blocks: int,
        max_model_len: int,
        watermark: float = 0.01,
    ) -> None:
        self.block_size = block_size
        self.num_total_gpu_blocks = num_gpu_blocks
        self.max_model_len = max_model_len

        self.watermark = watermark
        assert watermark >= 0.0

        self.watermark_blocks = int(watermark * num_gpu_blocks)
        self.gpu_allocator = BlockAllocator(block_size, num_gpu_blocks)
        # Mapping: seq_id -> BlockTable.
        self.block_tables: Dict[str, BlockTable] = {}

    def can_allocate_blocks(self, num_required_blocks: int) -> bool:
        num_free_gpu_blocks = self.gpu_allocator.get_num_free_blocks()
        # Use watermark to avoid frequent cache eviction.
        return num_free_gpu_blocks - num_required_blocks >= self.watermark_blocks

    def allocate(self, seq: Sequence, num_blocks: int) -> None:
        # Allocate new physical token blocks that will store the prompt tokens.
        block_table: BlockTable = []
        for _ in range(num_blocks):
            block = self.gpu_allocator.allocate()
            block_table.append(block)

        self.block_tables[seq.seq_id] = block_table

    def allocate_delta(self, seq: Sequence, total_num_blocks: int) -> None:
        # Allocate new physical token blocks that will store the prompt tokens.
        if seq.seq_id not in self.block_tables:
            self.allocate(seq, total_num_blocks)
            return

        num_existing_blocks = len(self.block_tables[seq.seq_id])
        num_new_blocks = total_num_blocks - num_existing_blocks
        for _ in range(num_new_blocks):
            block = self.gpu_allocator.allocate()
            self.block_tables[seq.seq_id].append(block)

    def can_append_slot(self) -> bool:
        num_free_gpu_blocks = self.gpu_allocator.get_num_free_blocks()
        return num_free_gpu_blocks > 0

    def append_slot(self, seq: Sequence, num_total_blocks: int) -> bool:
        """
        Allocate a physical slot for a new token.
        It returns True if a new block is allocated.
        """
        logical_blocks = seq.logical_token_blocks
        block_table = self.block_tables[seq.seq_id]

        if num_total_blocks < len(logical_blocks):
            # The sequence has a new logical block.
            # Allocate a new physical block.
            block = self.gpu_allocator.allocate()
            block_table.append(block)
            return True

        return False

    def _free_block_table(self, block_table: BlockTable) -> None:
        for block in set(block_table):
            self.gpu_allocator.free(block)

    def free(self, seq: Sequence) -> None:
        if seq.seq_id not in self.block_tables:
            # Already freed or haven't been scheduled yet.
            return
        block_table = self.block_tables[seq.seq_id]
        self._free_block_table(block_table)
        del self.block_tables[seq.seq_id]

    def get_block_table(self, seq: Sequence) -> List[int]:
        return self.block_tables[seq.seq_id]

    def is_allocated(self, seq: Sequence) -> bool:
        return seq.seq_id in self.block_tables
