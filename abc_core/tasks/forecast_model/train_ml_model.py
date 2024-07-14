import logging
from typing import Dict, List, Tuple
import pandas as pd

from abc_core.tasks.base_task import Task
from abc_core.utils.model_utils import get_model, tune_hyperparameters
from abc_core.utils.read_write import read_file, write_file

logger = logging.getLogger(__name__)


class TrainSklearnModel(Task):
    """Fit sklearn ml model to training data."""

    name = "train_ml_model"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config
        self.input_data = config.data.output_data
        self.output_data = config.data.output_data

    def run(self):
        train_data = self._load_inputs()

        fit = self._train_model(data=train_data)

        self._save_results(fit_obj=fit)

        return {"model_fit": fit}

    def _load_inputs(self, **kwargs) -> pd.DataFrame:
        """."""
        logger.info("Loading feature data table.")
        train_data = read_file(
            read_type="python_dict",
            base_directory=self.input_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.input_data.dicts.train_data,
        )
        return train_data

    def _save_results(self, fit_obj):
        """."""
        logger.info("Writing sklearn model fit object to file.")
        write_file(
            out_obj=fit_obj,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.models.ml_model,
        )

    def _train_model(self, data: pd.DataFrame):
        """Orchestration method."""
        X_train, X_test = data["X_train"], data["X_test"]
        y_train, y_test = data["y_train"], data["y_test"]

        logger.info("Hyperparameter tuning.")
        model_config = self.config.forecast_model.ml_model
        best_params, best_score = tune_hyperparameters(X_train=X_train, y_train=y_train, model_config=model_config)

        logger.info("Fit machine learning model.")
        model_name = self.config.forecast_model.ml_model.model_name
        model_tuned = get_model(model_params=best_params, model_name=model_name)
        model_tuned.fit(X_train, y_train)

        logger.info("Extract fit parameters from model.")
        # TODO!
        
        return model_tuned