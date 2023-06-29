import logging


def Logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # define handler and formatter
    stdout_handler = logging.StreamHandler()  # This for stdout logging
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)2d - %(message)s | %(processName)s: %(process)d | %(threadName)s:%(thread)d")

    # add formatter to handler
    stdout_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(stdout_handler)

    return logger


app_logger = Logger("app")
