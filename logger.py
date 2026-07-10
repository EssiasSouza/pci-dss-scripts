"""
logger.py

Logging configuration for PCI DSS Evidence Scanner.
"""

import logging
import os
from datetime import datetime


LOG_DIRECTORY = "logs"


def create_log_file():
    """
    Creates the log directory and returns the generated log file path.
    """

    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    log_file = os.path.join(
        LOG_DIRECTORY,
        f"PCI-DSS_evidences_{timestamp}.log"
    )

    return log_file


def setup_logger():
    """
    Configures application logger.
    """

    log_file = create_log_file()

    logger = logging.getLogger("PCI-DSS_Evidence_Scanner")

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def log_operation(logger, message):
    """
    Records a standard application operation.
    """

    logger.info(message)


def log_error(logger, message):
    """
    Records an application error.
    """

    logger.error(message)