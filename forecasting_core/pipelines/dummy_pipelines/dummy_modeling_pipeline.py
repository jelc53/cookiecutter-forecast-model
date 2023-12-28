import logging
from typing import Dict

from ac_availability_core.pipelines.core.base_pipeline import Pipeline
from ac_availability_core.tasks.dummy_tasks.forecasting.dummy_modeling import CreateDummyModelingOutput

logger = logging.getLogger(__name__)


class DummyModelingPipeline(Pipeline):
    name = "dummy_modeling"

    def __init__(self, config: Dict):
        self._tasks = self.get_tasks(config)
        super().__init__(config)

        self._parameters = {
            "config": config,
        }

    def get_tasks(self, config):
        pipeline_config = config.pipelines.dummy_modeling.tasks
        return ((CreateDummyModelingOutput, pipeline_config.create_dummy_modeling),)
