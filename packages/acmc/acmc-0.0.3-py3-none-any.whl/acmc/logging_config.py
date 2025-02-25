import pandas as pd
import logging

DEFAULT_LOG_FILE = "acmc.log"


# TODO: Determine if bcolours is still needed considering use of logging not print
class bcolors:  # for printing coloured text
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def setup_logger(log_level=logging.INFO):
    """Sets up logger as a singleton outputing to file and sysout syserr"""
    # Create a logger
    logger = logging.getLogger("acmc_logger")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        # Create a file handler that logs to a file
        file_handler = logging.FileHandler(DEFAULT_LOG_FILE)
        file_handler.setLevel(logging.INFO)

        # Create a stream handler that prints to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        # Create a formatter for how the log messages should look

        # Add the formatter to both handlers
        file_formatter = logging.Formatter(
            "%(asctime)s - - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        stream_formatter = logging.Formatter("[%(levelname)s] - %(message)s")
        stream_handler.setFormatter(stream_formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger


def set_log_level(log_level):
    """Sets the log level for the acmc logger"""
    logger = logging.getLogger("acmc_logger")
    logger.setLevel(log_level)  # Set logger level

    # Also update handlers to match the new level
    for handler in logger.handlers:
        handler.setLevel(log_level)
