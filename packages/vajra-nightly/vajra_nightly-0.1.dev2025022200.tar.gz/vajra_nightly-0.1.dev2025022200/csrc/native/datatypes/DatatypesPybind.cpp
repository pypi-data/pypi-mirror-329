#include "DatatypesPybind.h"
#include "SequenceMetadata.h"
//==============================================================================
void InitDatatypesPybindSubmodule(py::module_& pm)
{
  auto m = pm.def_submodule("datatypes", "Datatypes submodule");

  py::class_<vajra::SequenceMetadata>(m, "SequenceMetadata")
      .def(
          py::init<
              std::size_t,
              std::string&,
              std::size_t,
              std::size_t,
              std::vector<std::size_t>&,
              std::vector<std::size_t>&,
              bool>(),
          py::arg("schedule_id"),
          py::arg("seq_id"),
          py::arg("num_q_tokens"),
          py::arg("num_kv_tokens"),
          py::arg("block_table"),
          py::arg("kvp_group_ids"),
          py::arg("save_kv_cache"))
      .def("__str__", &vajra::SequenceMetadata::ToString)
      .def("__repr__", &vajra::SequenceMetadata::ToString)
      .def_readonly("schedule_id", &vajra::SequenceMetadata::m_nScheduleId)
      .def_readonly("seq_id", &vajra::SequenceMetadata::m_strSeqId)
      .def_readonly("num_q_tokens", &vajra::SequenceMetadata::m_nNumQTokens)
      .def_readonly("num_kv_tokens", &vajra::SequenceMetadata::m_nNumKvTokens)
      .def_readonly("block_table", &vajra::SequenceMetadata::m_vnBlockTable)
      .def_readonly("kvp_group_ids", &vajra::SequenceMetadata::m_vnKvpGroupIds)
      .def_readonly("save_kv_cache", &vajra::SequenceMetadata::m_bSaveKvCache)
      .def_readonly(
          "is_kvp_request",
          &vajra::SequenceMetadata::m_bIsKvpRequest);
}
//==============================================================================