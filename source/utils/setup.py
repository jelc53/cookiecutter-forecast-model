import logging

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    # ASCII Art Generator : https://patorjk.com/software/taag/
    # ToDo banner
    banner = r"""
          __               __     _          __  __                 __         ____
   ____ _/ /_  ____  _____/ /_   (_)___     / /_/ /_  ___     _____/ /_  ___  / / /
  / __ `/ __ \/ __ \/ ___/ __/  / / __ \   / __/ __ \/ _ \   / ___/ __ \/ _ \/ / / 
 / /_/ / / / / /_/ (__  ) /_   / / / / /  / /_/ / / /  __/  (__  ) / / /  __/ / /  
 \__, /_/ /_/\____/____/\__/  /_/_/ /_/   \__/_/ /_/\___/  /____/_/ /_/\___/_/_/   
/____/                                                                             

    """
    logger.info(banner)
