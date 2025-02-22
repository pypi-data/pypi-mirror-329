#pragma once

#include <torch/all.h>
#include <torch/csrc/distributed/c10d/ProcessGroup.hpp>

#include "Logging.h"
#include "StdCommon.h"
//==============================================================================
namespace vajra
{
//==============================================================================
class ProcessGroupWrapper
{
public:
  ProcessGroupWrapper(
      c10::intrusive_ptr<c10d::ProcessGroup> spTensorModelParallelGroup,
      c10::intrusive_ptr<c10d::ProcessGroup> spPipelineModelParallelGroup,
      c10::intrusive_ptr<c10d::ProcessGroup> spKvParallelGroup);

  c10::intrusive_ptr<c10d::ProcessGroup> GetTensorModelParallelGroup() const;
  c10::intrusive_ptr<c10d::ProcessGroup> GetPipelineModelParallelGroup() const;
  c10::intrusive_ptr<c10d::ProcessGroup> GetKvParallelGroup() const;

private:
  c10::intrusive_ptr<c10d::ProcessGroup> m_spTensorModelParallelGroup;
  c10::intrusive_ptr<c10d::ProcessGroup> m_spPipelineModelParallelGroup;
  c10::intrusive_ptr<c10d::ProcessGroup> m_spKvParallelGroup;
};
//==============================================================================
} // namespace vajra
//==============================================================================