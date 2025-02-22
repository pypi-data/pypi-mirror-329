#include <torch/csrc/distributed/c10d/ProcessGroup.hpp>

#include "AttentionWrapper.h"
#include "LinearLayers.h"
#include "Llama.h"
#include "ModelExecutorPybind.h"
#include "NormLayers.h"
#include "ProcessGroupWrapper.h"
#include "RotaryEmbedding.h"
//==============================================================================
namespace pybind11
{
namespace detail
{
template <> struct type_caster<std::set<int>>
{
public:
  PYBIND11_TYPE_CASTER(std::set<int>, _("Set[int]"));
  bool load(handle src, bool)
  {
    if (!py::isinstance<py::set>(src) && !py::isinstance<py::frozenset>(src))
      return false;
    for (auto item : src)
    {
      if (!py::isinstance<py::int_>(item))
        return false;
      value.insert(item.cast<int>());
    }
    return true;
  }
  static handle cast(const std::set<int>& src, return_value_policy, handle)
  {
    py::set s;
    for (int v : src)
      s.add(py::cast(v));
    return s.release();
  }
};
} // namespace detail
} // namespace pybind11
//==============================================================================
void InitModelExecutorPybindSubmodule(py::module_& pm)
{
  auto m = pm.def_submodule("model_executor", "Model executor submodule");

  pybind11::class_<vajra::LlamaMLP, std::shared_ptr<vajra::LlamaMLP>>(
      m,
      "LlamaMLP")
      .def(pybind11::init<
           std::shared_ptr<vajra::ColumnParallelLinear>,
           std::shared_ptr<vajra::RowParallelLinear>>())
      .def("forward", &vajra::LlamaMLP::Forward);

  pybind11::
      class_<vajra::LlamaAttention, std::shared_ptr<vajra::LlamaAttention>>(
          m,
          "LlamaAttention")
          .def(pybind11::init<
               int,
               int,
               float,
               std::shared_ptr<vajra::ColumnParallelLinear>,
               std::shared_ptr<vajra::RowParallelLinear>,
               std::shared_ptr<vajra::RotaryEmbedding>,
               std::shared_ptr<vajra::AttentionWrapper>>())
          .def("forward", &vajra::LlamaAttention::Forward);

  pybind11::class_<
      vajra::LlamaDecoderLayer,
      std::shared_ptr<vajra::LlamaDecoderLayer>>(m, "LlamaDecoderLayer")
      .def(pybind11::init<
           std::shared_ptr<vajra::LlamaAttention>,
           std::shared_ptr<vajra::LlamaMLP>,
           std::shared_ptr<vajra::RMSNorm>,
           std::shared_ptr<vajra::RMSNorm>>())
      .def("forward", &vajra::LlamaDecoderLayer::Forward);

  pybind11::class_<vajra::LlamaModel, std::shared_ptr<vajra::LlamaModel>>(
      m,
      "LlamaModel")
      .def(pybind11::init<
           std::shared_ptr<vajra::VocabParallelEmbedding>,
           std::vector<std::shared_ptr<vajra::LlamaDecoderLayer>>,
           std::shared_ptr<vajra::RMSNorm>>())
      .def("forward", &vajra::LlamaModel::Forward);

  pybind11::class_<
      vajra::ColumnParallelLinear,
      std::shared_ptr<vajra::ColumnParallelLinear>>(m, "ColumnParallelLinear")
      .def(pybind11::init<
           int,
           int,
           bool,
           int,
           bool,
           torch::Tensor,
           std::optional<torch::Tensor>,
           std::shared_ptr<vajra::ProcessGroupWrapper>>())
      .def("forward", &vajra::ColumnParallelLinear::Forward);

  pybind11::class_<
      vajra::RowParallelLinear,
      std::shared_ptr<vajra::RowParallelLinear>>(m, "RowParallelLinear")
      .def(pybind11::init<
           int,
           int,
           bool,
           bool,
           int,
           int,
           bool,
           torch::Tensor,
           std::optional<torch::Tensor>,
           std::shared_ptr<vajra::ProcessGroupWrapper>>())
      .def("forward", &vajra::RowParallelLinear::Forward);

  pybind11::class_<
      vajra::VocabParallelEmbedding,
      std::shared_ptr<vajra::VocabParallelEmbedding>>(
      m,
      "VocabParallelEmbedding")
      .def(pybind11::init<
           int,
           int,
           int,
           int,
           bool,
           int,
           int,
           int,
           torch::Tensor,
           std::shared_ptr<vajra::ProcessGroupWrapper>>())
      .def("forward", &vajra::VocabParallelEmbedding::Forward);

  pybind11::class_<vajra::RMSNorm, std::shared_ptr<vajra::RMSNorm>>(
      m,
      "RMSNorm")
      .def(pybind11::init<torch::Tensor, double>())
      .def("forward", &vajra::RMSNorm::Forward);

  pybind11::
      class_<vajra::RotaryEmbedding, std::shared_ptr<vajra::RotaryEmbedding>>(
          m,
          "RotaryEmbedding")
          .def(pybind11::init<int, int, long, long, bool, torch::Tensor>())
          .def("forward", &vajra::RotaryEmbedding::Forward);

  pybind11::class_<
      vajra::ProcessGroupWrapper,
      std::shared_ptr<vajra::ProcessGroupWrapper>>(m, "ProcessGroupWrapper")
      .def(pybind11::init<
           c10::intrusive_ptr<c10d::ProcessGroup>,
           c10::intrusive_ptr<c10d::ProcessGroup>,
           c10::intrusive_ptr<c10d::ProcessGroup>>())
      .def(
          "get_tensor_model_parallel_group",
          &vajra::ProcessGroupWrapper::GetTensorModelParallelGroup)
      .def(
          "get_pipeline_model_parallel_group",
          &vajra::ProcessGroupWrapper::GetPipelineModelParallelGroup)
      .def(
          "get_kv_parallel_group",
          &vajra::ProcessGroupWrapper::GetKvParallelGroup);
}
//==============================================================================