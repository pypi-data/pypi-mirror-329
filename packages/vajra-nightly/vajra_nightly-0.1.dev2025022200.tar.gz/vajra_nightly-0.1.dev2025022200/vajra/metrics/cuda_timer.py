# type: ignore
# torch.cuda.Event has weird typing, so we need to ignore it
from typing import Optional

import torch

from vajra.metrics.constants import OperationMetrics
from vajra.metrics.metrics_store import MetricsStore

USE_CUDA_EVENTS = True


class CudaTimer:

    def __init__(
        self,
        name: Optional[OperationMetrics],
        layer_id: Optional[int] = None,
        rank: Optional[int] = None,
    ):
        self.name = name
        self.metrics_store = MetricsStore.get_instance()
        self.layer_id = layer_id
        self.disabled = (self.name is None) or not self.metrics_store.is_op_enabled(
            metric_name=self.name, layer_id=layer_id, rank=rank
        )

        if self.disabled:
            return

        self.profiler = torch.profiler.profile(
            activities=[torch.profiler.ProfilerActivity.CUDA],
            on_trace_ready=self.handle_trace,
        )
        self.start_event: Optional[torch.cuda.Event] = None
        self.end_event: Optional[torch.cuda.Event] = None

    def __enter__(self):
        if self.disabled:
            return

        if USE_CUDA_EVENTS:
            self.start_event = torch.cuda.Event(enable_timing=True)
            # assume thread safety here
            self.start_event.record()  # type: ignore
        else:
            self.profiler.__enter__()

        return self

    def handle_trace(self, trace):
        assert self.name is not None

        total_cuda_time = sum([e.cuda_time_total for e in trace.key_averages()])

        self.metrics_store.push_operation_metrics(
            self.name,
            total_cuda_time * 1e-3,  # convert to ms
        )

    def __exit__(self, *args):
        if self.disabled:
            return

        assert self.name is not None

        if USE_CUDA_EVENTS:
            self.end_event = torch.cuda.Event(enable_timing=True)
            # assume thread safety here
            self.end_event.record()  # type: ignore
            self.metrics_store.push_operation_metrics_events(
                self.name, self.start_event, self.end_event
            )
        else:
            self.profiler.__exit__(*args)
