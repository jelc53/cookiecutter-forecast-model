import logging
from typing import Dict

import pandas as pd
from source.tasks.base_task import Task
from source.utils.data_loading_and_writing import read_file, write_file

from source.schema.dummy_data import DummyData

logger = logging.getLogger(__name__)


class FeatureEngineering(Task):
    """Prepares custom features used in forecast model."""

    name = "feature_engineering"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config
        self.input_data = config.data.processed_data
        self.output_data = config.data.output_data

    def run(self):
        in_df = self._load_inputs()

        out_df = self._process_data(df=in_df)

        self._save_results(out_df=out_df)

        return {"dummy_data": out_df}

    def _load_inputs(self, **kwargs):
        """."""
        logger.info("Loading raw data table.")
        df = read_file(
            schema=DummyData,
            base_directory=self.input_data.base_directory,
            time_connector=self.config.run_details.processed_data_version,
            file_name=self.input_data.tables.dummy_data,
        )

        return df

    def _save_results(self, out_df):
        """."""
        logger.info("Writing dummy table to file.")
        write_file(
            df=out_df,
            base_directory=self.output_data.base_directory,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.tables.dummy_data,
        )

    def _prepare_data(df: pd.DataFrame) -> pd.DataFrame:
        """Orchestration method."""
        logger.info("Processing real estate dataset.")
        return df.copy()