from typing import Any

from vajra.core.scheduler.base_scheduler import BaseScheduler, BatchFormationTracker
from vajra.datatypes import Sequence


class FcfsFixedChunkScheduler(BaseScheduler):
    def _get_seq_next_num_q_tokens(
        self, seq: Sequence, batch_formation_tracker: BatchFormationTracker
    ) -> int:
        assert not seq.is_finished()
        assert not seq.prompt_stage_processing_finished

        active_kvp_group_ids = self._get_active_kvp_group_ids(seq)
        batched_num_q_tokens_across_groups = (
            batch_formation_tracker.get_q_tokens_for_kvp_groups(active_kvp_group_ids)
        )
        max_num_q_tokens_across_groups = max(batched_num_q_tokens_across_groups)

        num_processed_tokens = seq.get_num_prompt_tokens_stage_processed()

        next_num_tokens = min(
            seq.prompt_len - num_processed_tokens,
            self.scheduler_config.chunk_size - max_num_q_tokens_across_groups,
        )

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
