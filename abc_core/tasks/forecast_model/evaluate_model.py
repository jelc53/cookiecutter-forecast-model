import logging
from typing import Dict, List, Tuple
import pandas as pd

from abc_core.tasks.base_task import Task
from abc_core.utils.model_utils import get_model, tune_hyperparameters
from abc_core.utils.read_write import read_file, write_file

logger = logging.getLogger(__name__)


class EvaluateForecastModel(Task):
    """Evaluate forecasting model using test set."""

    name = "evaluate_model"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config
        self.input_data = config.data.output_data
        self.output_data = config.data.output_data

    def run(self):
        model_tuned, train_data = self._load_inputs()

        metrics_dict = self._evaluate_metrics(model=model_tuned, data=train_data)

        self._save_results(fit_obj=fit)

        return {"fit_metrics": metrics_dict}

    def _load_inputs(self, **kwargs):
        """."""
        logger.info("Loading feature data table.")
        model_tuned = read_file(
            read_type="sklearn_model",
            base_directory=self.input_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.input_data.models.ml_model,
        )
        train_data = read_file(
            read_type="python_dict",
            base_directory=self.input_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.input_data.dicts.train_data,
        )
        return model_tuned, train_data

    def _save_results(self, metrics_dict: dict):
        """."""
        logger.info("Writing fit metrics to file.")
        write_file(
            out_obj=metrics_dict,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.dicts.fit_metrics,
        )

    def _evaluate_metrics(self, model, data: pd.DataFrame):
        """Orchestration method."""
        X_train, X_test = data["X_train"], data["X_test"]
        y_train_true, y_test_true = data["y_train"], data["y_test"]

        logger.info("Get predictions for the test set.")
        y_test_pred = model_tuned.predict(X_test)
        y_train_pred = model_tuned.predict(X_train)

        logger.info("Calculate fit metrics.")
        # ...
        
        return model_tuned