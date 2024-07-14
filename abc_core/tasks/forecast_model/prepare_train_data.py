import logging
from typing import Dict, List, Tuple
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from abc_core.tasks.base_task import Task
from abc_core.utils.read_write import read_file, write_file

logger = logging.getLogger(__name__)


class PrepareTrainingData(Task):
    """Prepares train and test data used in forecast model."""

    name = "prepare_training_data"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config
        self.input_data = config.data.output_data
        self.output_data = config.data.output_data

    def run(self):
        feature_df = self._load_inputs()

        train_data = self._prepare_data(df=feature_df)

        self._save_results(train_data=train_data)

        return {"train_data": train_data}

    def _load_inputs(self, **kwargs) -> pd.DataFrame:
        """."""
        logger.info("Loading feature data table.")
        feature_df = read_file(
            base_directory=self.input_data.base_directory,
            pipeline_name=self.config.run_details.pipeline,
            time_connector=self.config.run_details.processed_data_version,
            file_name=self.input_data.tables.feature_data,
        )
        return feature_df

    def _save_results(self, train_data: Dict):
        """."""
        logger.info("Writing training data dict to file.")
        write_file(
            out_obj=train_data,
            pipeline_name=self.config.run_details.pipeline,
            base_directory=self.output_data.base_directory,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.dicts.train_data,
        )

    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Orchestration method."""
        target = self.config.forecast_model.target
        numeric_features = self.config.forecast_model.features.numeric
        categorical_features = self.config.forecast_model.features.categorical

        logger.info("Select feature variables to be used.")
        X = self.select_training_features(df=df, numeric_features=numeric_features, categorical_features=categorical_features)
        y = df[target].copy()

        logger.info("Split into train vs test datasets.")
        (X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.33, random_state=42)

        logger.info("Scaling numeric predictor variables.")
        # TODO : encode and concatenate categorical variables
        X_train_scaled, X_test_scaled = self.scale_numeric_features(X_train=X_train, X_test=X_test, numeric_features=numeric_features)
        
        logger.info("Format output to match specified model type.")
        model_type = self.config.forecast_model.model_type
        train_data = self.format_train_data_output(X_train=X_train_scaled, X_test=X_test_scaled, y_train=y_train, y_test=y_test, model_type=model_type)

        return train_data

    def select_training_features(self, df: pd.DataFrame, numeric_features: List[str], categorical_features: List[str]) -> pd.DataFrame:
        """Select the features to be used in the training data."""
        # TODO : encode and concatenate categorical variables
        selected_features = numeric_features # + categorical_features
        return df[selected_features].copy()

    def scale_numeric_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame, numeric_features: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Apply sklearn's standard scaler to X_train and X_test."""
        scaler = StandardScaler()
        X_train_scaled_arr = scaler.fit_transform(X_train[numeric_features])
        X_test_scaled_arr = scaler.transform(X=X_test[numeric_features])
        X_train_scaled = pd.DataFrame(X_train_scaled_arr, columns=numeric_features)
        X_test_scaled = pd.DataFrame(X_test_scaled_arr, columns=numeric_features)
        return X_train_scaled, X_test_scaled

    def format_train_data_output(self, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.DataFrame, y_test: pd.DataFrame, model_type: str) -> Dict:
        """Populate output dictionary."""
        if model_type == "ml_model":
            return {
                "X_train": X_train,
                "X_test": X_test,
                "y_train": y_train,
                "y_test": y_test,
            }
        elif model_type == "bayesian":
            return {} #TODO!
        else:
            raise ValueError(f"Model type {model_type} not supported by this task.")
