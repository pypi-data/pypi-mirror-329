# Vajra

[![Publish Nightly Build to PyPI](https://github.com/project-vajra/vajra/actions/workflows/publish_nightly.yml/badge.svg)](https://github.com/project-vajra/vajra/actions/workflows/publish_nightly.yml)
[![Publish Release to PyPI](https://github.com/project-vajra/vajra/actions/workflows/publish_release.yml/badge.svg)](https://github.com/project-vajra/vajra/actions/workflows/publish_release.yml)
[![Deploy Documentation](https://github.com/project-vajra/vajra/actions/workflows/deploy_docs.yml/badge.svg)](https://github.com/project-vajra/vajra/actions/workflows/deploy_docs.yml)
[![Functional Test Suite](https://github.com/project-vajra/vajra/actions/workflows/functional_test_suite.yml/badge.svg)](https://github.com/project-vajra/vajra/actions/workflows/functional_test_suite.yml)
[![Run Linters](https://github.com/project-vajra/vajra/actions/workflows/lint.yml/badge.svg)](https://github.com/project-vajra/vajra/actions/workflows/lint.yml)

The second-wave lean distributed low-latency LLM inference serving engine.

## Setup

### Setup CUDA

Vajra has been tested with CUDA 12.6 on A100 and H100 GPUs.

### Clone repository

```sh
git clone --recursive -j8 https://github.com/project-vajra/vajra
```

### Create mamba environment

Setup mamba if you don't already have it,

```sh
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh # follow the instructions from there
```

Create a Python 3.10 environment with cmake,

```sh
mamba env create -f environment-dev.yml -p ./env
```

Activate the environment,

```sh
mamba activate ./env
```

### Install Vajra

```sh
make build
```

### Incremental C++ Builds

To perform incremental native builds, use the following commands:

```sh
make build_native_incremental
```

### Linting & formatting

For linting code,

```sh
make lint 
```

You can simplify life by performing auto-formatting,

```sh
make format
```

### Running Test

```
make test
```

## Citation

If you use our work, please consider citing our papers:

```
@article{agrawal2024mnemosyne,
  title={Mnemosyne: Parallelization strategies for efficiently serving multi-million context length llm inference requests without approximations},
  author={Agrawal, Amey and Chen, Junda and Goiri, {\'I}{\~n}igo and Ramjee, Ramachandran and Zhang, Chaojie and Tumanov, Alexey and Choukse, Esha},
  journal={arXiv preprint arXiv:2409.17264},
  year={2024}
}

@article{agrawal2024taming,
  title={Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve},
  author={Agrawal, Amey and Kedia, Nitin and Panwar, Ashish and Mohan, Jayashree and Kwatra, Nipun and Gulavani, Bhargav S and Tumanov, Alexey and Ramjee, Ramachandran},
  journal={Proceedings of 18th USENIX Symposium on Operating Systems Design and Implementation, 2024, Santa Clara},
  year={2024}
}
```

## Acknowledgment

We learned a lot and reused code from [vLLM](https://vllm-project.github.io/) and [SGLang](https://github.com/sgl-project/sglang).