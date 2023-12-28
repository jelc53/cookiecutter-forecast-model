from typing import Dict

# Naive pipeline
from ac_availability_core.pipelines.dummy_pipelines.dummy_processing_pipeline import DummyDataCubePipeline
from ac_availability_core.pipelines.dummy_pipelines.dummy_modeling_pipeline import DummyModelingPipeline


# DS Core pipelines to be implemented

# Building a registry of known pipeline.
PIPELINE_REGISTRY = {cls.name: cls for cls in [DummyDataCubePipeline, DummyModelingPipeline]}


def run_pipeline(pipeline: str, config: Dict):
    """Run the selected pipeline E2E.

    :param pipeline: Name of the pipeline to run
    :type pipeline: str
    :param config: `config` object created from the yml configuration files
    :type config: Config
    :raises NotImplementedError: Exception when an invalid `pipeline` param value is provided
    :return: Output of the pipeline's `run` method
    :rtype: Any
    """
    if pipeline in PIPELINE_REGISTRY:
        pipeline_class_name = PIPELINE_REGISTRY[pipeline]
        pipeline_to_run = pipeline_class_name(config=config)
    else:
        raise NotImplementedError(f"Pipeline {pipeline} is not implemented yet")

    res = pipeline_to_run.run()
    return res
