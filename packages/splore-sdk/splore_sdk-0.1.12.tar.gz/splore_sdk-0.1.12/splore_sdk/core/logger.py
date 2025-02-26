import logging
import os

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def setup_logger(name: str, log_level: str = 'info'):
    """
    Sets up the logger for the SDK with configurable log levels.
    :param name: The name of the logger (usually the module name)
    :param log_level: The log level to set. Can be 'debug', 'info', 'warning', 'error', or 'critical'.
    :return: logger instance
    """

    log_level = LOG_LEVELS.get(log_level.lower(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)


    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

sdk_logger = setup_logger('splore_sdk', log_level=os.getenv('SDK_LOG_LEVEL', 'info'))
