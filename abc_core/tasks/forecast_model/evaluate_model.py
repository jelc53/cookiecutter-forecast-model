import logging
from typing import Dict, List, Tuple
import pandas as pd

from abc_core.tasks.base_task import Task
from abc_core.utils.read_write import read_file, write_file
from abc_core.utils.evaluate import get_accuracy_metrics

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

        pred_train_df, pred_test_df, metrics = self._evaluate_metrics(model=model_tuned, data=train_data)

        self._save_results(pred_train_df=pred_train_df, pred_test_df=pred_test_df, metrics=metrics)

        return {"fit_metrics": metrics}

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

    def _save_results(self, metrics: dict, pred_train_df: pd.DataFrame, pred_test_df: pd.DataFrame):
        """."""
        logger.info("Writing fit metrics to file.")
        write_file(
            out_obj=metrics,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.dicts.fit_metrics,
        )
        write_file(
            out_obj=pred_train_df,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.tables.predict_train,
        )
        write_file(
            out_obj=pred_test_df,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.tables.predict_test,
        )

    def _evaluate_metrics(self, model, data: pd.DataFrame, metrics: dict = {}):
        """Orchestration method."""
        X_train, X_test = data["X_train"], data["X_test"]
        y_train, y_test = data["y_train"], data["y_test"]

        logger.info("Get predictions for the test set.")
        pred_train_df = pd.DataFrame({"y_true": y_train, "y_pred": model.predict(X_train)})
        pred_test_df = pd.DataFrame({"y_true": y_test, "y_pred": model.predict(X_test)})

        logger.info("Calculate fit metrics.")
        metrics = get_accuracy_metrics(metrics, pred_train_df, "train")
        metrics = get_accuracy_metrics(metrics, pred_test_df, "test")
        
        return pred_train_df, pred_test_df, metrics