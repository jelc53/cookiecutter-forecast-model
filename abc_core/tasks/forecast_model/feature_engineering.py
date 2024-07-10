import logging
from typing import Dict

import pandas as pd
from abc_core.tasks.base_task import Task
from abc_core.utils.read_write import read_file, write_file

from abc_core.schema.dummy_data import DummyData
from abc_core.constant import name as n
from math import radians, cos, sin, asin, sqrt

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

        out_df = self._create_features(df=in_df)

        self._save_results(out_df=out_df)

        return {"feature_data": out_df}

    def _load_inputs(self, **kwargs) -> pd.DataFrame:
        """."""
        logger.info("Loading processed data table.")
        df = read_file(
            schema=DummyData,
            base_directory=self.input_data.base_directory,
            time_connector=self.config.run_details.processed_data_version,
            file_name=self.input_data.tables.dummy_data,
        )

        return df

    def _save_results(self, out_df):
        """."""
        logger.info("Writing feature variables table to file.")
        write_file(
            out_obj=out_df,
            pipeline_name=self.config.run_details.pipeline,
            base_directory=self.output_data.base_directory,
            time_connector=self.config.run_details.run_version,
            file_name=self.output_data.tables.feature_data,
        )

    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Orchestration method."""
        logger.info("Adding feature: haversine point combines lat and lng.")
        df[n.F_HAVERSINE_POINT] = self.single_pt_haversine(lat=df[n.F_X5_LATITUDE], lng=df[n.F_X6_LONGITUDE])

        # logger.info("Adding feature: [xx].")
        # NOTE: add new feature variables here!
        
        return df

    def single_pt_haversine(self, lat, lng, degrees=True):
        """
        'Single-point' Haversine: Calculates the great circle distance
        between a point on Earth and the (0, 0) lat-long coordinate
        """
        r = 6371 # Earth's radius (km). Have r = 3956 if you want miles

        # Convert decimal degrees to radians
        if degrees:
            lat, lng = map(radians, [lat, lng])

        # 'Single-point' Haversine formula
        a = sin(lat/2)**2 + cos(lat) * sin(lng/2)**2
        d = 2 * r * asin(sqrt(a)) 

        return d
