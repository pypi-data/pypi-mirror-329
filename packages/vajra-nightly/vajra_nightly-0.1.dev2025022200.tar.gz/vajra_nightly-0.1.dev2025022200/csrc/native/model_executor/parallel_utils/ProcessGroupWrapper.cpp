#include "ProcessGroupWrapper.h"
//==============================================================================
using namespace vajra;
//==============================================================================
ProcessGroupWrapper::ProcessGroupWrapper(
    c10::intrusive_ptr<c10d::ProcessGroup> spTensorModelParallelGroup,
    c10::intrusive_ptr<c10d::ProcessGroup> spPipelineModelParallelGroup,
    c10::intrusive_ptr<c10d::ProcessGroup> spKvParallelGroup)
    : m_spTensorModelParallelGroup(spTensorModelParallelGroup),
      m_spPipelineModelParallelGroup(spPipelineModelParallelGroup),
      m_spKvParallelGroup(spKvParallelGroup)
{
}
//==============================================================================
c10::intrusive_ptr<c10d::ProcessGroup>
ProcessGroupWrapper::GetTensorModelParallelGroup() const
{
  return m_spTensorModelParallelGroup;
}
//==============================================================================
c10::intrusive_ptr<c10d::ProcessGroup>
ProcessGroupWrapper::GetPipelineModelParallelGroup() const
{
  return m_spPipelineModelParallelGroup;
}
//==============================================================================
c10::intrusive_ptr<c10d::ProcessGroup>
ProcessGroupWrapper::GetKvParallelGroup() const
{
  return m_spKvParallelGroup;
}
//==============================================================================
