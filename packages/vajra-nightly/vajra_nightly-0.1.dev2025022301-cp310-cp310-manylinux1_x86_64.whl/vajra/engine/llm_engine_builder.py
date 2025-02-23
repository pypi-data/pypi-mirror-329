from vajra.config import SystemConfig
from vajra.engine.base_llm_engine import BaseLLMEngine
from vajra.engine.pipeline_parallel_llm_engine import PipelineParallelLLMEngine


class LLMEngineBuilder:

    @classmethod
    def from_system_config(cls, config: SystemConfig) -> "BaseLLMEngine":
        """Creates an LLM engine from the engine arguments"""
        if config.parallel_config.pipeline_parallel_size > 1:
            llm_engine = PipelineParallelLLMEngine(config)
        else:
            llm_engine = BaseLLMEngine(config)

        return llm_engine
