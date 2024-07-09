import logging
from typing import Dict

from source.pipelines.core.base_pipeline import Pipeline
from source.tasks.data_processing.process_dataset import ProcessDataset

logger = logging.getLogger(__name__)


class DataProcessingPipeline(Pipeline):
    """Data processing pipeline."""

    name = "data_processing_pipeline"

    def __init__(self, config: Dict):
        self._tasks = self.get_tasks(config)
        super().__init__(config)

        self._parameters = {
            "config": config,
        }

    def get_tasks(self, config):
        pipeline_config = config.pipelines.data_processing.tasks
        return (ProcessDataset, pipeline_config.process_dataset)
