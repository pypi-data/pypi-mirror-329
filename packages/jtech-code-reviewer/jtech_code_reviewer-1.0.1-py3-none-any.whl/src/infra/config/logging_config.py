import inspect
import logging.config

import yaml
from dotenv import load_dotenv

from src.infra.config.constants import Constants

# Load environment variables from a .env file
load_dotenv()

# Load logging configuration from a YAML file and configure logging
with open(Constants.LOGGING_CONFIG, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger():
    """
    Retrieves a logger instance for the calling module.

    The logger name is derived from the module name of the caller.

    Returns:
        logging.Logger: A logger instance for the calling module.
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    logger_name = module.__name__ if module else '__main__'
    return logging.getLogger(logger_name)
