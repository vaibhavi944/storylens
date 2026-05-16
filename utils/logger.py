# ====================================================
# FILE PURPOSE
# ====================================================
# Provides centralized logging configuration for StoryLens.
# This ensures that all parts of the application output consistent,
# formatted log messages to track pipeline execution and debugging.

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
