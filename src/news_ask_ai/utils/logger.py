import logging
from logging.handlers import RotatingFileHandler




def setup_logger(level: int = logging.INFO, log_file: str = "app.log") -> logging.Logger:
    """
    Set up a logger with the specified name, log file, and level.

    Args:
        name (str): Name of the logger.
        log_file (str): File to write logs to. Defaults to 'app.log'.
        level (int): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(level)

    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
