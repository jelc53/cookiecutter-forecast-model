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

        fit, params = self._train_model(data=train_data)

        self._save_results(fit_obj=fit, params=params)

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

    def _save_results(self, fit_obj, params):
        """."""
        logger.info("Writing sklearn model fit object to file.")
        write_file(
            out_obj=fit_obj,
            base_directory=self.output_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.models.ml_model,
        )
        model_name = self.config.forecast_model.ml_model.model_name
        if model_name == "lin_reg" or model_name == "log_reg":
            write_file(
                out_obj=params,
                base_directory=self.output_data.base_directory,
                pipeline_name=self.config.run_details.pipeline,
                time_connector=self.config.run_details.run_version,
                file_name=self.output_data.tables.fit_params,
            )
        else:  # black box models
            write_file(
                out_obj=params,
                base_directory=self.output_data.base_directory,
                pipeline_name=self.config.run_details.pipeline,
                time_connector=self.config.run_details.run_version,
                file_name=self.output_data.tables.feature_importance,
            )

    def _train_model(self, data: pd.DataFrame):
        """Orchestration method."""
        X_train, X_test = data["X_train"], data["X_test"]
        y_train, y_test = data["y_train"], data["y_test"]
        model_name = self.config.forecast_model.ml_model.model_name
        
        logger.info(f"Hyperparameter tuning for {model_name} model.")
        best_params = self.find_best_hyperparameters(X_train=X_train, y_train=y_train)

        logger.info(f"Fit model with {best_params}.")
        model_tuned = get_model(model_params=best_params, model_name=model_name)
        model_tuned.fit(X_train, y_train)

        logger.info("Extract coefficients from model.")
        params = self.extract_features_from_model(model=model_tuned)
        
        return model_tuned, params

    def find_best_hyperparameters(self, X_train: pd.DataFrame, y_train: pd.DataFrame):
        """Helper method to collect hyperparameters for selected model."""
        model_name = self.config.forecast_model.ml_model.model_name
        model_config = self.config.forecast_model.ml_model
        if model_name == "lin_reg" or model_name == "log_reg":
            best_params = model_config.hyperparameters[model_name]
            best_params = None if best_params == 'None' else best_params
        else:
            best_params, _ = tune_hyperparameters(X_train=X_train, y_train=y_train, model_config=model_config)
        return best_params

    def extract_features_from_model(self, model) -> pd.DataFrame:
        """Extract learned coefficients or feature importances from model."""
        model_name = self.config.forecast_model.ml_model.model_name
        numeric_features = self.config.forecast_model.features.numeric
        # categorical_features = self.config.forecast_model.features.categorical
        features = numeric_features #+ categorical_features
        if model_name == "lin_reg" or model_name == "log_reg":
            values = model.coef_
        else: # black box models
            values = model.feature_importances_
        return pd.DataFrame({"param": features, "value": values})