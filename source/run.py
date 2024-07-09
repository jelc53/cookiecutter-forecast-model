import logging
import click
from typing import List, Tuple, Union

import source.constant.name as n
from source.utils.parser import read_yaml_files
from source.utils.setup import setup_logging
from source.pipelines.pipeline_manager import run_pipeline
from source.utils.versioning import (
    get_versioning_in_config,
    save_config_as_yml,
)


# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

DEFAULT_CONFIG_FILES = [
    "configs/*.yml",
]
@click.command()
@click.option(
    "--config",
    default=(),
    multiple=True,
    help="Extra configuration files",
)
@click.option("--pipeline", "-p", default="training", help="name of the pipeline to run", required=True)
@click.option(
    "--run_version",
    help="Manually setting run version code, default: timestamp",
    required=False,
)
@click.option(
    "--processed_data_version",
    help="Manually setting run version code, default: timestamp",
    required=False,
)
@click.option(
    "--raw_data_version",
    help="Manually setting run version code, default: timestamp",
    required=False,
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def main(
    pipeline: str,
    config: Union[Tuple[str], List[str]],
    run_version: str,
    processed_data_version: str,
    verbose: bool,
):
    setup_logging(verbose=verbose)
    config = read_yaml_files(list(config))

    # set up run info:
    run_info = {
        n.F_PIPELINE: pipeline,
        n.F_RUN_VERSION: run_version,
        n.F_PROCESSED_DATA_VERSION: processed_data_version,
    }
    config = get_versioning_in_config(run_info=run_info, config=config)

    try:
        run_pipeline(
            pipeline,
            config,
        )
    except Exception as e:
        raise e

    finally:
        save_config_as_yml(config=config)
        logging.warning(str(config.run_details.to_dict()))



if __name__ == "__main__":
    main()
