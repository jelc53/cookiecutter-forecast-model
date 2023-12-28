import logging

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    # ASCII Art Generator : https://patorjk.com/software/taag/
    # ToDo banner
    banner = r"""  ____     __       ____  __ __   ____  ____  _       ____  ____   ____  _      ____  ______  __ __ 
 /    |   /  ]     /    ||  |  | /    ||    || |     /    ||    \ |    || |    |    ||      ||  |  |
|  o  |  /  /     |  o  ||  |  ||  o  | |  | | |    |  o  ||  o  ) |  | | |     |  | |      ||  |  |
|     | /  /      |     ||  |  ||     | |  | | |___ |     ||     | |  | | |___  |  | |_|  |_||  ~  |
|  _  |/   \_     |  _  ||  :  ||  _  | |  | |     ||  _  ||  O  | |  | |     | |  |   |  |  |___, |
|  |  |\     |    |  |  | \   / |  |  | |  | |     ||  |  ||     | |  | |     | |  |   |  |  |     |
|__|__| \____|    |__|__|  \_/  |__|__||____||_____||__|__||_____||____||_____||____|  |__|  |____/ 
    """
    logger.info(banner)
