import logging
from typing import Dict

import pandas as pd
from abc_core.tasks.base_task import Task
from abc_core.utils.read_write import read_file, write_file
from abc_core.utils.transform import apply_schema, handle_datetime_dtype

from abc_core.schema.dummy_data import DummyData
from abc_core.constant import name as n

logger = logging.getLogger(__name__)


class ProcessDummyData(Task):
    """Loads raw data and outputs it."""

    name = "process_dummy_data"

    def __init__(
        self,
        config: Dict,
        **args,
    ):
        self.config = config
        self.input_data = config.data.raw_data
        self.output_data = config.data.processed_data

    def run(self):
        in_df = self._load_inputs()

        out_df = self._process_data(df=in_df)

        self._save_results(df=out_df)

        return {"dummy_data": out_df}

    def _load_inputs(self, **kwargs) -> pd.DataFrame:
        """."""
        logger.info("Loading raw dummy data table.")
        df = read_file(
            base_directory=self.input_data.base_directory,
            time_connector=self.config.run_details.raw_data_version,
            file_name=self.input_data.tables.dummy_data,
        )

        return df

    def _save_results(self, df: pd.DataFrame):
        """."""
        logger.info("Writing processed dummy table to file.")
        write_file(
            out_obj=df,
            base_directory=self.output_data.base_directory,
            time_connector=self.config.run_details.processed_data_version,
            file_name=self.output_data.tables.dummy_data,
        )

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Orchestration method."""
        logger.info("Rename columns to match designated schema.")
        df = self.rename_sales_columns(df=df)
        
        logger.info("Dataset specific cleaning steps.")
        # NOTE: future developers to add any required cleaning steps
        # ...

        logger.info("Handle typing for date columns.")
        df = handle_datetime_dtype(df=df, col=n.F_X1_TRANSACTION_DATE, format="%Y-%m-%d")

        logger.info("Apply schema to processed data.")
        df = apply_schema(df=df, schema=DummyData)
        
        return df
    
    # NOTE: to be over-written by future developers
    def rename_sales_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rename columns to match designated schema."""
        column_mapping = {  # NOTE: see dummy_data.py for schema
            "x1_transaction_date": n.F_X1_TRANSACTION_DATE,
            "x2_house_age": n.F_X2_HOUSE_AGE,
            "x3_distance_to_the_nearest_mrt_station": n.F_X3_DISTANCE_TO_NEAREST_STATION,
            "x4_number_of_convenience_stores": n.F_X4_NUMBER_OF_CONVENIENCE_STORES,
            "x5_latitude": n.F_X5_LATITUDE,
            "x6_longitude": n.F_X6_LONGITUDE,
            "y_house_price_of_unit_area": n.F_Y_HOUSE_PRICE_OF_UNIT_AREA,
        }
        df = df.rename(columns=column_mapping, errors="raise")
        return df
