# postfix_watcher/logging.py
import logging
from logging.handlers import SysLogHandler

def get_logger():
    logger = logging.getLogger("postfix_watcher")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        syslog_handler = SysLogHandler(address="/dev/log")
        syslog_handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s %(message)s'))
        logger.addHandler(syslog_handler)

        # Optional stderr for debugging
        if __debug__:
            stderr_handler = logging.StreamHandler()
            stderr_handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s %(message)s'))
            logger.addHandler(stderr_handler)
    return logger
