#include <torch/extension.h>

#include "DatatypesPybind.h"
#include "ModelExecutorPybind.h"
//==============================================================================
PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
  InitDatatypesPybindSubmodule(m);
  InitModelExecutorPybindSubmodule(m);
}
//==============================================================================