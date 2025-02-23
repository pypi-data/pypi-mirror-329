from dataclasses import dataclass
from typing import List

from .sequence_schedule_metadata import SequenceScheduleMetadata


@dataclass(frozen=True)
class SchedulerOutput:
    id: int
    ignored_seq_ids: List[str]
    preempted_seq_ids: List[str]
    seq_schedule_metadata_list: List[SequenceScheduleMetadata]

    @property
    def is_empty(self) -> bool:
        return not self.seq_schedule_metadata_list

    @property
    def has_no_output(self) -> bool:
        return (
            not self.seq_schedule_metadata_list
            and not self.ignored_seq_ids
            and not self.preempted_seq_ids
        )
