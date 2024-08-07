import logging
from typing import Dict

from abc_core.pipelines.core.base_pipeline import Pipeline
from abc_core.tasks.data_processing.process_dummy_data import ProcessDummyData

logger = logging.getLogger(__name__)


class DataProcessingPipeline(Pipeline):
    """Data processing pipeline."""

    name = "data_processing"

    def __init__(self, config: Dict):
        self._tasks = self.get_tasks(config)
        super().__init__(config)

        self._parameters = {
            "config": config,
        }

    def get_tasks(self, config):
        pipeline_config = config.pipelines.data_processing.tasks
        return (
            (ProcessDummyData, pipeline_config.process_dummy_data),
            # (ProcessNewData, pipeline_config.process_new_data),
        )
