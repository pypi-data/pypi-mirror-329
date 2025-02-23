# Copyright 2023 The Vajra team.
# Adapted from https://github.com/NVIDIA/Megatron-LM/blob/main/megatron/core/tensor_parallel/mappings.py
# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.

import torch

from vajra.metrics.constants import OperationMetrics
from vajra.metrics.cuda_timer import CudaTimer
from vajra.model_executor.parallel_utils.parallel_state import (
    get_kv_parallel_group,
    get_kv_parallel_world_size,
    get_pipeline_model_parallel_group,
    get_pipeline_model_parallel_next_rank,
    get_pipeline_model_parallel_prev_rank,
    get_tensor_model_parallel_group,
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
)

from .utils import split_tensor_along_last_dim


def reduce_from_kv_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """All-reduce the input tensor across model parallel group."""

    # Bypass the function if we are using only 1 GPU.
    if get_kv_parallel_world_size() == 1:
        return input_

    # All-reduce.
    torch.distributed.all_reduce(input_, group=get_kv_parallel_group())

    return input_


def reduce_from_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """All-reduce the input tensor across model parallel group."""

    # Bypass the function if we are using only 1 GPU.
    if get_tensor_model_parallel_world_size() == 1:
        return input_

    # All-reduce.
    torch.distributed.all_reduce(input_, group=get_tensor_model_parallel_group())

    return input_


def scatter_to_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """Split the tensor along its last dimension and keep the
    corresponding slice."""

    world_size = get_tensor_model_parallel_world_size()
    # Bypass the function if we are using only 1 GPU.
    if world_size == 1:
        return input_

    # Split along last dimension.
    input_list = split_tensor_along_last_dim(input_, world_size)

    # Note: torch.split does not create contiguous tensors by default.
    rank = get_tensor_model_parallel_rank()
    output = input_list[rank].contiguous()

    return output


def gather_from_group(
    input_: torch.Tensor,
    world_size: int,
    rank: int,
    group: torch.distributed.ProcessGroup,
    concat_dim: int,
) -> torch.Tensor:
    # Bypass the function if we are using only 1 GPU.
    assert world_size > 1

    tensor_list = [torch.empty_like(input_) for _ in range(world_size)]
    tensor_list[rank] = input_
    torch.distributed.all_gather(tensor_list, input_, group=group)

    # Note: torch.cat already creates a contiguous tensor.
    output = torch.cat(tensor_list, dim=concat_dim).contiguous()
    return output


def gather_from_tensor_model_parallel_region(input_: torch.Tensor) -> torch.Tensor:
    """Gather tensors and concatenate along the last dimension."""

    world_size = get_tensor_model_parallel_world_size()
    # Bypass the function if we are using only 1 GPU.
    if world_size == 1:
        return input_

    # Size and dimension.
    last_dim = input_.dim() - 1
    rank = get_tensor_model_parallel_rank()
    group = get_tensor_model_parallel_group()

    return gather_from_group(input_, world_size, rank, group, last_dim)


def send_to_next_pipeline_stage(
    hidden_states: torch.Tensor, enable_pipeline_tp_comm_opt: bool = True
) -> None:
    """Send hidden states to the next pipeline stage using partial send + allgather.

    Instead of sending the full tensor, each rank sends only its partition
    to the next pipeline stage, followed by an allgather to reconstruct
    the full tensor.
    """
    # Bypass if single stage
    if get_pipeline_model_parallel_group().size() == 1:
        return

    tp_world_size = get_tensor_model_parallel_world_size()
    tp_rank = get_tensor_model_parallel_rank()
    next_rank = get_pipeline_model_parallel_next_rank()

    last_dim_size = hidden_states.size()[-1]

    with CudaTimer(OperationMetrics.NCCL_SEND):
        # Split tensor along last dim if optimization is enabled
        if (
            tp_world_size > 1
            and last_dim_size % tp_world_size == 0
            and enable_pipeline_tp_comm_opt
        ):
            tensor_chunks = split_tensor_along_last_dim(hidden_states, tp_world_size)
            # Send only this rank's chunk
            chunk_to_send = tensor_chunks[tp_rank].contiguous()
            torch.distributed.send(
                tensor=chunk_to_send,
                dst=next_rank,
                group=get_pipeline_model_parallel_group(),
            )
        else:
            # No splitting needed if optimization disabled or other conditions not met
            torch.distributed.send(
                tensor=hidden_states,
                dst=next_rank,
                group=get_pipeline_model_parallel_group(),
            )


def recv_from_last_pipeline_stage(
    hidden_states: torch.Tensor, enable_pipeline_tp_comm_opt: bool = True
) -> torch.Tensor:
    """Receive hidden states from previous pipeline stage using partial recv + allgather."""
    if get_pipeline_model_parallel_group().size() == 1:
        return hidden_states

    tp_world_size = get_tensor_model_parallel_world_size()
    tp_rank = get_tensor_model_parallel_rank()
    prev_rank = get_pipeline_model_parallel_prev_rank()

    last_dim_size = hidden_states.size()[-1]

    with CudaTimer(OperationMetrics.NCCL_RECV):
        if (
            tp_world_size > 1
            and last_dim_size % tp_world_size == 0
            and enable_pipeline_tp_comm_opt
        ):
            # Calculate chunk size
            chunk_size = last_dim_size // tp_world_size

            # Create shape tuple for the chunk tensor
            chunk_shape = hidden_states.size()[:-1] + (chunk_size,)

            # Receive this rank's chunk
            chunk = torch.empty(
                size=chunk_shape, dtype=hidden_states.dtype, device=hidden_states.device
            )
            torch.distributed.recv(
                tensor=chunk,
                src=prev_rank,
                group=get_pipeline_model_parallel_group(),
            )

            # Allgather to reconstruct full tensor
            tp_group = get_tensor_model_parallel_group()
            hidden_states = gather_from_group(
                chunk, tp_world_size, tp_rank, tp_group, concat_dim=-1
            )
        else:
            # Fallback: receive full tensor if optimization disabled or other conditions not met
            torch.distributed.recv(
                tensor=hidden_states,
                src=prev_rank,
                group=get_pipeline_model_parallel_group(),
            )

    return hidden_states
