from typing import Dict

# import pipelines here
from source.pipelines.core.data_processing_pipeline import DataProcessingPipeline
from source.pipelines.core.forecast_model_pipeline import ForecastModelPipeline

# build a registry of known pipeline.
PIPELINE_REGISTRY = {cls.name: cls for cls in [DataProcessingPipeline, ForecastModelPipeline]}


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
