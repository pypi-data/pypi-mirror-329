from dataclasses import dataclass
from typing import List, Optional

from .sequence import Sequence
from .sequence_status import SequenceStatus


@dataclass(frozen=True)
class RequestOutput:
    """The output data of a request to the LLM.

    Args:
        seq: The output sequences of the request.
        outputs: The output sequences of the request.
        finished: Whether the whole request is finished.
    """

    seq: Sequence
    finished: bool
    finish_reason: Optional[str] = None

    @classmethod
    def from_seq(cls, seq: Sequence) -> "RequestOutput":
        return cls(
            seq,
            seq.is_finished(),
            SequenceStatus.get_finished_reason(seq.status),
        )

    @property
    def text(self) -> str:
        return self.seq.output_text

    @property
    def seq_id(self) -> str:
        return self.seq.seq_id

    @property
    def prompt(self) -> str:
        return self.seq.prompt

    @property
    def prompt_token_ids(self) -> List[int]:
        return self.seq.prompt_token_ids

    @property
    def token_ids(self) -> List[int]:
        return self.seq.output_token_ids
