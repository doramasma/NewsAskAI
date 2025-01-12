import logging


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name, log file, and level.

    Args:
        name (str): Name of the logger.
        log_file (str): File to write logs to. Defaults to 'app.log'.
        level (int): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger.
    """
    # Create a logger
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(level)

    # Create a console handler for outputting logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Define a log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    return logger
