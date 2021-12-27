"""
Created on 2021-09-21 by Peter Ciaccia
Contains common functions used for several test scripts, like reading and writing methods
"""

import time
from functools import wraps
import logging
from dotenv import load_dotenv

import log.conf

load_dotenv()
logger = log.conf.get_logger()


def timer(task, *args, **kwargs):
    """
    decorator function that times other functions
    :param task:
    :param args:
    :param kwargs:
    :return:
    """
    if logger.level < logging.DEBUG:
        return task(*args, **kwargs)

    @wraps(task)
    def wrap(*args, **kwargs):
        start_time = time.time()
        task_complete = task(*args, **kwargs)
        end_time = time.time()
        logger.debug(f'task "{task.__name__}" (args: {args} kwargs: {kwargs}) '
                     f'took {end_time-start_time:.6f} s')
        return task_complete
    return wrap


def log_ten_powers(powers):
    """
    Pass an iterable of ints by which 10 is exponentiated
    :param powers: iterable of ints by which 10 is exponentiated
    :return ten_powers: list of powers of ten
    """

    ten_powers = [10**ten_log for ten_log
                  in powers
                  if 10**ten_log % 1]

    return ten_powers
