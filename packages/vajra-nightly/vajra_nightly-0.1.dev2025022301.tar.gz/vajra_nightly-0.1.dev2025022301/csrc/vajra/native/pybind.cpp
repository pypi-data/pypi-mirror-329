#include <torch/extension.h>

#include "vajra/native/datatypes/DatatypesPybind.h"
#include "vajra/native/model_executor/ModelExecutorPybind.h"
//==============================================================================
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
  InitDatatypesPybindSubmodule(m);
  InitModelExecutorPybindSubmodule(m);
}
//==============================================================================
