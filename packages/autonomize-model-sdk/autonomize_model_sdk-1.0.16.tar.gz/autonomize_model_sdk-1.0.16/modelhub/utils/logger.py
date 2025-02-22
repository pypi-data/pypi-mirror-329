""" This module contains the logger setup function. """

import logging
import os
import sys
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """
    A custom log formatter that adds a timestamp and label to log records.

    This formatter extends the base `logging.Formatter` class and overrides the `format` method
    to add a timestamp and label to each log record.

    Attributes:
        None

    Methods:
        format(record): Formats the log record by adding a timestamp and label.

    Usage:
        formatter = CustomFormatter()
        handler.setFormatter(formatter)
    """

    def format(self, record):
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
        record.label = f"[{os.environ.get('APP_NAME', 'genesis')}]"
        return super().format(record)


def setup_logger(name):
    """
    Set up a logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger object.

    """
    logger = logging.getLogger(name)

    # Set log level from environment variable
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        log_handler = logging.StreamHandler(sys.stdout)
        formatter = CustomFormatter(
            fmt="%(timestamp)s %(label)s %(levelname)s: %(message)s"
        )
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)

    return logger
