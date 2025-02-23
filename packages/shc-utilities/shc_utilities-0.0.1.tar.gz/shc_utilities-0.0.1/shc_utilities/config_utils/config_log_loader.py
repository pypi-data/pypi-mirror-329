import logging
import json
import os
from typing import Optional

# Set _CONFIG_PATH Env variable
config_path = os.getenv('_CONFIG_PATH', "config.json")

# Flag variables to check if config and logging are already set up
config_initialized = False
logging_initialized = False

# Default Configuration object
default_config = {
    "logging": {
        "format": "%(asctime)s [%(levelname)s] -> [%(threadName)s] - %(funcName)s - %(lineno)d - %(message)s ",
        "mode": "info",
        "folder_path": "log",
        "file_name": "output"
    }
}
# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format=default_config.get('logging').get('format')
)
config: Optional[dict] = None
logger: Optional[logging.Logger] = None

# Function to load the configuration from config.json


def load_config(config_path):
    global config, config_initialized

    # If config is already initialized, return the existing config
    if config_initialized:
        return config

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        config_initialized = True
        logging.info("Config Initialized ...")
        return config
    except FileNotFoundError:
        logging.warning(
            "Config JSON file not found. Please set the _CONFIG_PATH environment variable. Using default config for logging.")
        return default_config
    except json.JSONDecodeError:
        logging.error(
            f"Error decoding JSON in configuration file '{config_path}'.")
        raise  # Reraise the error after logging it
    except Exception as e:
        logging.error(f"Unexpected error while loading configuration: {e}")
        raise  # Reraise the error after logging it


def get_log_level(level):
    level = level.lower()
    if level == "info":
        return logging.INFO
    elif level == "debug":
        return logging.DEBUG
    elif level == "trace":
        return logging.CRITICAL

# initialize log


def setup_logging(config=None, file_name=None):
    import datetime

    global logger, logging_initialized

    # If logging is already initialized, return the existing logger
    if logging_initialized:
        return logger

    # Default Config
    config = config if config != None else default_config
    try:
        file_name = file_name if file_name != None else config.get(
            'logging', default_config.get('logging')).get('file_name')
        log_format = config.get(
            'logging', default_config.get('logging')).get('format')
        log_formatter = logging.Formatter(log_format)

        root_logger = logging.getLogger()
        root_logger.setLevel(get_log_level(config.get(
            'logging', default_config.get('logging')).get('mode')))
        if root_logger.handlers:
            root_logger.handlers.clear()

        console_handler = logging.StreamHandler()
        console_handler.setLevel(get_log_level(
            config.get('logging', default_config.get('logging')).get('mode')))
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

        file_date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
        log_dir = config.get('logging', default_config.get(
            'logging')).get('folder_path')

        # Create the directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_name = f"{file_name}_{file_date}.log"
        log_path = f"{log_dir}/{log_file_name}"
        logging.info(log_path)
        # logging.basicConfig(level=logging.INFO, filename=log_path, filemode="a", format=log_format)

        file_handler = logging.FileHandler(log_path, mode='a')
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)
        logging.info("Logger Initialized ...")
        return root_logger
    except KeyError as e:
        logging.error(f"Missing configuration key: {e}")
        raise  # Reraise the error after logging it
    except ValueError as e:
        logging.error(f"Invalid value in configuration: {e}")
        raise  # Reraise the error after logging it
    except Exception as e:
        logging.error(f"Unexpected error while setting up logging: {e}")
        raise  # Reraise the error after logging it


# Assuming load_config and setup_logging are defined elsewhere
def setup():
    try:
        config = load_config(config_path)
        logger = setup_logging(config)

        # Optionally, return both as a dictionary if you want
        result = {
            'config': config,
            'logger': logger
        }
    except Exception as e:
        # If an error occurs while loading config or setting up logging, log it and stop further execution
        logging.critical(
            f"Fatal error during configuration or logging setup: {e}")
        raise  # Stop execution if the configuration or logging setup fails

    # Expose config and logger for other modules to import
    return config, logger


# Load configuration and logger setup
config, logger = setup()

# Return both config and logger so they can be imported elsewhere
__all__ = ['config', 'logger']
