from typing import Optional

import torch
import torch.distributed
import zmq

from vajra.datatypes import (
    SamplerOutputs,
    SchedulerOutput,
    StepMicrobatchOutputs,
    StepOutputs,
)
from vajra.logger import init_logger
from vajra.utils.threading_utils import exit_on_error
from vajra.worker.base_worker import BaseWorker

logger = init_logger(__name__)


class PipelineParallelWorker(BaseWorker):
    """A worker class that executes (a partition of) the model on a GPU.

    Each worker is associated with a single GPU. The worker is responsible for
    maintaining the KV cache and executing the model on the GPU. In case of
    distributed inference, each worker is assigned a partition of the model.
    """

    def _init_zmq_sockets(self):
        super()._init_zmq_sockets()

        self.microbatch_socket = self.zmq_context.socket(zmq.PUSH)
        self.microbatch_socket.connect(
            f"tcp://{self.comm_info.engine_ip_address}:{self.comm_info.microbatch_socket_port}"
        )

    def _verify_parallel_config(self) -> None:
        assert self.config.parallel_config.pipeline_parallel_size > 1

    def on_step_completed(
        self,
        scheduler_output: SchedulerOutput,
        sampler_outputs: Optional[SamplerOutputs],
    ) -> None:
        assert self.seq_manager
        # in pipeline parallel case, each stage won't have sampler output
        # so we need to do the book keeping update later, here we just want to update the stuff for
        # this stage completion
        self.seq_manager.on_stage_completed(scheduler_output)

    @exit_on_error
    def _execution_loop(self) -> None:
        assert self.seq_manager

        torch.cuda.set_device(self.device)

        self.worker_ready_event.set()

        while True:
            step_inputs = self.enqueue_socket.recv_pyobj()

            for new_seq in step_inputs.new_seqs:
                # so that any state changes from scheduler are reset
                new_seq.reset_for_worker()
                self.seq_manager.add_seq(new_seq)

            for pending_step_output in step_inputs.pending_step_outputs:
                self.seq_manager.on_step_completed(
                    pending_step_output[
                        0
                    ].seq_schedule_metadata_list,  # scheduler_output
                    pending_step_output[1],  # sampler_outputs
                )

            output = self.execute_model(step_inputs.scheduler_output)

            if not self.is_tensor_parallel_rank_zero:
                continue

            if self.is_last_pipeline_stage:
                assert output

                logger.debug(
                    f"Worker {self.rank} sending output to engine: {output} for {step_inputs.scheduler_output}",
                )
                self.output_socket.send_pyobj(
                    StepOutputs(
                        step_inputs.scheduler_output.id,
                        output,
                    )
                )
            elif self.is_first_pipeline_stage:
                logger.debug(
                    f"Worker {self.rank} sending microbatch signal for {step_inputs.scheduler_output}",
                )
                self.microbatch_socket.send_pyobj(
                    StepMicrobatchOutputs(step_inputs.scheduler_output.id)
                )
