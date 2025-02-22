import time
from typing import Optional

from .sequence_status import SequenceStatus


class SequenceState:

    def __init__(self, id: str, arrived_at: float, num_prompt_tokens: int):
        self._id = id
        self._arrived_at: float = arrived_at
        self._num_prompt_tokens: int = num_prompt_tokens
        self._num_output_tokens: int = 0
        self._status = SequenceStatus.WAITING
        self._is_scheduled: bool = False
        self._is_completed: bool = False
        self._scheduled_at: Optional[float] = None
        self._completed_at: Optional[float] = None
        self._prompt_processing_completed_at: Optional[float] = None
        self._last_restart_at: Optional[float] = None
        self._last_pause_at: Optional[float] = None
        self._execution_time: float = 0.0
        self._preempted_time: float = 0.0
        self._last_execution_start_at: Optional[float] = None
        self._num_restarts: int = 0
        self._num_pauses: int = 0
        self._is_ignore_finished: bool = False
        self._last_token_generated_at: Optional[float] = None
        self._last_token_generation_time: float = 0.0

    @property
    def id(self) -> str:
        return self._id

    @property
    def num_prompt_tokens(self) -> int:
        return self._num_prompt_tokens

    @property
    def num_output_tokens(self) -> int:
        return self._num_output_tokens

    @property
    def num_total_tokens(self) -> int:
        return self._num_prompt_tokens + self._num_output_tokens

    @property
    def status(self) -> SequenceStatus:
        return self._status

    @property
    def is_scheduled(self) -> bool:
        return self._is_scheduled

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @property
    def arrived_at(self) -> float:
        return self._arrived_at

    @property
    def scheduled_at(self) -> float:
        assert self._scheduled_at is not None
        return self._scheduled_at

    @property
    def completed_at(self) -> float:
        assert self._completed_at is not None
        return self._completed_at

    @property
    def prompt_processing_completed_at(self) -> float:
        assert self._prompt_processing_completed_at is not None
        return self._prompt_processing_completed_at

    @property
    def e2e_time(self) -> float:
        assert self._completed_at is not None

        return self._completed_at - self._arrived_at

    @property
    def e2e_time_piecewise_normalized(self) -> float:
        scheduling_delay = self.scheduling_delay
        assert scheduling_delay is not None

        return scheduling_delay + (
            self.execution_plus_preemption_time / self._num_output_tokens
        )

    @property
    def e2e_time_normalized(self) -> float:
        e2e_time = self.e2e_time
        assert e2e_time is not None
        return e2e_time / self._num_output_tokens

    @property
    def e2e_prefill_time(self) -> float:
        assert self._prompt_processing_completed_at is not None
        return self._prompt_processing_completed_at - self._arrived_at

    @property
    def e2e_prefill_time_normalized(self) -> float:
        e2e_prefill_time = self.e2e_prefill_time
        assert e2e_prefill_time is not None and self._num_prompt_tokens
        return e2e_prefill_time / self._num_prompt_tokens

    @property
    def e2e_prefill_time_piecewise_normalized(self) -> float:
        scheduling_delay = self.scheduling_delay
        prefill_execution_plus_preemption_time = (
            self.prefill_execution_plus_preemption_time
        )

        assert (
            scheduling_delay is not None
            and prefill_execution_plus_preemption_time is not None
            and self._num_prompt_tokens
        )

        return scheduling_delay + (
            prefill_execution_plus_preemption_time / self._num_prompt_tokens
        )

    @property
    def prefill_execution_plus_preemption_time(self) -> float:
        assert (
            self._prompt_processing_completed_at is not None
            and self._scheduled_at is not None
        )
        return self._prompt_processing_completed_at - self._scheduled_at

    @property
    def decode_execution_plus_preemption_time(self) -> float:
        assert (
            self._completed_at is not None
            and self._prompt_processing_completed_at is not None
        )
        return self._completed_at - self._prompt_processing_completed_at

    @property
    def prefill_execution_plus_preemption_time_normalized(self) -> float:
        prefill_execution_plus_preemption_time = (
            self.prefill_execution_plus_preemption_time
        )

        assert (
            prefill_execution_plus_preemption_time is not None
            and self._num_prompt_tokens
        )

        return prefill_execution_plus_preemption_time / self._num_prompt_tokens

    @property
    def decode_execution_plus_preemption_time_normalized(self) -> float:
        decode_execution_plus_preemption_time = (
            self.decode_execution_plus_preemption_time
        )
        assert decode_execution_plus_preemption_time is not None
        return decode_execution_plus_preemption_time / self._num_output_tokens

    @property
    def scheduling_delay(self) -> float:
        assert self._scheduled_at is not None
        return self._scheduled_at - self._arrived_at

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @property
    def execution_time_normalized(self) -> float:
        return self.execution_time / self._num_output_tokens

    @property
    def preempted_time(self) -> float:
        return self._preempted_time

    @property
    def execution_plus_preemption_time(self) -> float:
        return self._execution_time + self._preempted_time

    @property
    def execution_plus_preemption_time_normalized(self) -> float:
        return self.execution_plus_preemption_time / self._num_output_tokens

    @property
    def last_token_generation_time(self) -> float:
        return self._last_token_generation_time

    @property
    def num_restarts(self) -> int:
        return self._num_restarts

    @property
    def num_pauses(self) -> int:
        return self._num_pauses

    @property
    def is_ignore_finished(self) -> bool:
        return self._is_ignore_finished

    def _handle_transitions_from_waiting_status(
        self, current_time: float, status: SequenceStatus
    ) -> None:
        if status == SequenceStatus.RUNNING:
            # request is starting execution now
            if self._scheduled_at is None:
                # running for the first time
                assert self._num_restarts == 0
                self._is_scheduled = True
                self._scheduled_at = current_time
            else:
                # restarting
                assert self._num_restarts > 0
                assert (
                    self._last_restart_at is not None
                ), "Cannot compute preempted_time if last_restart_at is None."
                self._preempted_time += current_time - self._last_restart_at

            self._last_execution_start_at = current_time
        elif status == SequenceStatus.FINISHED_IGNORED:
            self._is_ignore_finished = True
            self._is_completed = True
            self._completed_at = current_time
            # the scheduler will not schedule this request again
            self._scheduled_at = current_time
        else:
            raise ValueError(
                f"Invalid state transition from {self._status} to {status} for request {self._id}."
            )

    def _handle_transitions_from_running_status(
        self, current_time: float, status: SequenceStatus
    ) -> None:
        assert (
            self._last_execution_start_at is not None
        ), "Cannot compute execution time if _last_execution_start_at is None."
        self._execution_time += current_time - self._last_execution_start_at

        if status == SequenceStatus.PAUSED:
            self._num_pauses += 1
            self._last_pause_at = current_time
        elif status == SequenceStatus.WAITING_PREEMPTED:
            self._num_restarts += 1
            self._last_restart_at = current_time
        else:
            raise ValueError(
                f"Invalid state transition from {self._status} to {status} for request {self._id}."
            )

    def _handle_transitions_from_paused_status(
        self, current_time: float, status: SequenceStatus
    ) -> None:
        assert (
            self._last_pause_at is not None
        ), "Cannot compute preempted_time if _last_pause_at is None."
        self._preempted_time += current_time - self._last_pause_at

        if (
            status == SequenceStatus.FINISHED_STOPPED
            or status == SequenceStatus.FINISHED_LENGTH_CAPPED
        ):
            self._is_completed = True
            self._completed_at = current_time
        elif status == SequenceStatus.RUNNING:
            self._last_execution_start_at = current_time
        elif status == SequenceStatus.WAITING_PREEMPTED:
            self._num_restarts += 1
            self._last_restart_at = current_time
        else:
            raise ValueError(
                f"Invalid state transition from {self._status} to {status} for request {self._id}."
            )

    @status.setter
    def status(self, status: SequenceStatus) -> None:
        current_time = time.time()

        if (
            self._status == SequenceStatus.WAITING
            or self._status == SequenceStatus.WAITING_PREEMPTED
        ):
            self._handle_transitions_from_waiting_status(current_time, status)
        elif self._status == SequenceStatus.RUNNING:
            self._handle_transitions_from_running_status(current_time, status)
        elif self._status == SequenceStatus.PAUSED:
            self._handle_transitions_from_paused_status(current_time, status)
        else:
            raise ValueError(
                f"Invalid state transition from {self._status} to {status} for request {self._id}."
            )

        self._status = status

    def on_prompt_processing_completed(self) -> None:
        self._prompt_processing_completed_at = time.time()

    def on_token_generated(self) -> None:
        current_time = time.time()

        self._num_output_tokens += 1

        if self._last_token_generated_at is None:
            self._last_token_generation_time = 0.0
        else:
            self._last_token_generation_time = (
                current_time - self._last_token_generated_at
            )

        self._last_token_generated_at = current_time
