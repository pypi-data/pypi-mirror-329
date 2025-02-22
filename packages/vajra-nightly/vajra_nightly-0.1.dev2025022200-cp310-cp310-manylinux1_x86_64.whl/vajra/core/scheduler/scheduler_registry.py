from vajra.core.scheduler.edf_scheduler import EdfScheduler
from vajra.core.scheduler.fcfs_fixed_chunk_scheduler import FcfsFixedChunkScheduler
from vajra.core.scheduler.fcfs_scheduler import FcfsScheduler
from vajra.core.scheduler.lrs_scheduler import LrsScheduler
from vajra.core.scheduler.st_scheduler import StScheduler
from vajra.enums import SchedulerType
from vajra.utils.base_registry import BaseRegistry


class SchedulerRegistry(BaseRegistry):
    pass


SchedulerRegistry.register(SchedulerType.FCFS_FIXED_CHUNK, FcfsFixedChunkScheduler)
SchedulerRegistry.register(SchedulerType.FCFS, FcfsScheduler)
SchedulerRegistry.register(SchedulerType.EDF, EdfScheduler)
SchedulerRegistry.register(SchedulerType.LRS, LrsScheduler)
SchedulerRegistry.register(SchedulerType.ST, StScheduler)
