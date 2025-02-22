from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class SamplerOutput:
    """The model output associated with a sequence.

    Args:
        seq_id: The ID of sequence.
        output_token: The output token ID.
    """

    schedule_id: int
    seq_id: str
    output_tokens: Tuple[int, ...]


SamplerOutputs = List[Optional[SamplerOutput]]
