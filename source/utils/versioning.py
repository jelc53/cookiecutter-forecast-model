import os
import yaml
import logging

from typing import Dict
from box import Box
from datetime import datetime
from source.constant.mapping import PIPELINES_MAPPING
import source.constant.name as n

logger = logging.getLogger(__name__)


def get_versioning_in_config(run_info: Dict[str, str], config: Box) -> Box:
    """Add to the config versioning informations:
    - running pipeline name
    - processed_data_version
    - raw_data_version -- irrelevant for modeling pipelines
    - run_version
    These informations depend on the type of pipeline, either processing or modeling"""

    if run_info[n.F_PIPELINE] not in PIPELINES_MAPPING:
        raise ValueError(f"Pipeline {run_info['pipeline']} isn't defined as a proessing or modeling pipeline")

    config.run_details[n.F_PIPELINE] = run_info[n.F_PIPELINE]
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    config.run_details[n.F_RUN_VERSION] = (
        current_time if run_info[n.F_RUN_VERSION] is None else run_info[n.F_RUN_VERSION]
    )
    if PIPELINES_MAPPING[run_info[n.F_PIPELINE]] == "data_processing":
        config.run_details[n.F_PROCESSED_DATA_VERSION] = (
            current_time if run_info[n.F_PROCESSED_DATA_VERSION] is None else run_info[n.F_PROCESSED_DATA_VERSION]
        )

    elif PIPELINES_MAPPING[run_info[n.F_PIPELINE]] == "forecast_model":
        config.run_details[n.F_PROCESSED_DATA_VERSION] = (
            get_latest_timestamp(config.data.processed_data.base_directory)
            if run_info[n.F_PROCESSED_DATA_VERSION] is None
            else run_info[n.F_PROCESSED_DATA_VERSION]
        )
        
    return config


def get_latest_timestamp(folder_path: str) -> str:
    """Return latest timestamp associated to a folder"""
    subfolders = [f.path.split("/")[-1] for f in os.scandir(folder_path) if f.is_dir()]
    if len(subfolders) == 0:
        raise ValueError(f"Folder {folder_path} is empty")
    return max(subfolders)


def save_config_as_yml(config: Box):
    path = "artefacts/output/" + PIPELINES_MAPPING[config.run_details.pipeline] + "/" + config.run_details.run_version
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "config.yml"), "w") as outfile:
        yaml.dump(config.to_dict(), outfile)
    return
