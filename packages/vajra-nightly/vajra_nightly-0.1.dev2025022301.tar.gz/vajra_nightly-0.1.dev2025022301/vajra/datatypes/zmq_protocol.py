from dataclasses import dataclass
from typing import List, Optional, Tuple

from .sampler_output import SamplerOutputs
from .scheduler_output import SchedulerOutput
from .sequence import Sequence


@dataclass(frozen=True)
class StepInputs:
    """Input data for a single step of the model.

    Attributes:
        scheduler_output: The outputs from the scheduler for this step.
        new_seqs: A list of new sequences to add to the engine
        pending_step_outputs: A list of tuples of scheduler outputs and sampler outputs
    """

    scheduler_output: SchedulerOutput
    new_seqs: Optional[List[Sequence]] = None
    pending_step_outputs: Optional[List[Tuple[SchedulerOutput, SamplerOutputs]]] = None


@dataclass(frozen=True)
class StepMicrobatchOutputs:
    schedule_id: int


@dataclass(frozen=True)
class StepOutputs:
    schedule_id: int
    sampler_outputs: SamplerOutputs
