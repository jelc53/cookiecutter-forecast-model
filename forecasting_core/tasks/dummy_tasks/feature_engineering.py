import logging
from typing import Dict
import os

import pandas as pd
from ac_availability_core.tasks.base_task import Task
from ac_availability_core.utils.data_loading_and_writing import read_file, write_file

logger = logging.getLogger(__name__)


class CreateDummyDataCube(Task):
    """Loads raw data and outputs it"""

    name = "dummy_data_cube"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config

    def _load_inputs(self, **kwargs):
        logger.info("Loading raw table")
        self.raw_data_config = self.config.data.raw_data
        df_maintenance = read_file(
            base_directory=self.raw_data_config.base_directory,
            time_connector=self.config.run_details.raw_data_version,
            file_name=self.raw_data_config.tables.icw_maintenance_backward,
        )

        return df_maintenance

    def run(self):
        df_maintenance = self._load_inputs()
        self._save_results(df=df_maintenance)
        return {"df_maintenance": df_maintenance}

    def _save_results(self, df):
        logger.info("Writing dummy table")
        processed_data_config = self.config.data.processed_data
        write_file(
            df=df,
            base_directory=processed_data_config.base_directory,
            time_connector=self.config.run_details.processed_data_version,
            file_name=processed_data_config.tables.dummy_maintenance,
        )
