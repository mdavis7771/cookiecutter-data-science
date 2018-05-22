# -*- coding: utf-8 -*-
# Decorators
from functools import wraps
import logging
import logging.config
import io
import os


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''

    def __init__(self, my_logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = my_logger
        self.level = level or logging.INFO

    def write(self,buf):
        self.buf = buf.strip('\r\n\t ')

    def flush(self):
        self.logger.log(self.level, self.buf)


def config_logging():
    # load the logging configuration
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.ini'))


def log_func(orig_func):

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info(
            '{} ran with args: {}, and kwargs: {}'.format(orig_func.__name__, args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper


def time_func(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        logger = logging.getLogger(__name__)
        logger.info('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result

    return wrapper