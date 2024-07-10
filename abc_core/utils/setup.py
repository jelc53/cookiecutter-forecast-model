import logging
import os
from logging.config import dictConfig
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def setup_logger(filename: Union[Path, str] = None) -> None:
    """Configure logging module."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "basic": {
                "format": "[%(asctime)s][%(levelname)-8s]" + "[%(name)s:%(lineno)d[%(funcName)s] %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
            "colored": {
                "()": "coloredlogs.ColoredFormatter",
                "format": "[%(asctime)s][%(levelname)-8s]" + "[%(name)s:%(lineno)d[%(funcName)s] %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }

    if filename is not None:
        filename = Path(filename)
        filename.parent.mkdir(exist_ok=True, parents=True)
        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "formatter": "basic",
            "level": "INFO",
            "encoding": "utf8",
            "filename": filename,
            "mode": "a",
        }
        for logger_config in config["loggers"].values():
            logger_config["handlers"] += ["file"]

    dictConfig(config=config)


def setup_logging(config: dict) -> str:
    log_base_directory_main = config.log_details.base_directory.main_directory
    log_base_directory_logs = config.log_details.base_directory.logs_directory
    log_file_name = config.log_details.file_name
    log_file_ext = config.log_details.file_ext
    run_version = config.run_details.run_version
    pipeline = config.run_details.pipeline
    log_filepath = os.path.join(
        log_base_directory_main,
        log_base_directory_logs,
        pipeline,
        log_file_name + "_" + run_version + log_file_ext,
    )
    setup_logger(filename=f"{log_filepath}")

    # ASCII Art Generator : https://patorjk.com/software/taag/
    banner = r"""
          __               __     _          __  __                 __         ____
   ____ _/ /_  ____  _____/ /_   (_)___     / /_/ /_  ___     _____/ /_  ___  / / /
  / __ `/ __ \/ __ \/ ___/ __/  / / __ \   / __/ __ \/ _ \   / ___/ __ \/ _ \/ / / 
 / /_/ / / / / /_/ (__  ) /_   / / / / /  / /_/ / / /  __/  (__  ) / / /  __/ / /  
 \__, /_/ /_/\____/____/\__/  /_/_/ /_/   \__/_/ /_/\___/  /____/_/ /_/\___/_/_/   
/____/                                                                             

    """
    logger.info(banner)
    return log_filepath
