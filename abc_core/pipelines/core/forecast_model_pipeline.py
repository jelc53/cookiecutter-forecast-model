import logging
from typing import Dict

from abc_core.pipelines.core.base_pipeline import Pipeline
from abc_core.tasks.forecast_model.feature_engineering import FeatureEngineering
from abc_core.tasks.forecast_model.prepare_train_data import PrepareTrainingData
from abc_core.tasks.forecast_model.train_ml_model import TrainSklearnModel
from abc_core.tasks.forecast_model.evaluate_model import EvaluateForecastModel

logger = logging.getLogger(__name__)


class ForecastModelPipeline(Pipeline):
    """Forecast model pipeline."""

    name = "forecast_model"

    def __init__(self, config: Dict):
        self._tasks = self.get_tasks(config)
        super().__init__(config)

        self._parameters = {
            "config": config,
        }

    def get_tasks(self, config):
        pipeline_config = config.pipelines.forecast_model.tasks
        return (
            (FeatureEngineering, pipeline_config.feature_engineering),
            (PrepareTrainingData, pipeline_config.prepare_train_data),
            (TrainSklearnModel, pipeline_config.train_ml_model),
            (EvaluateForecastModel, pipeline_config.evaluate_model),
        )
