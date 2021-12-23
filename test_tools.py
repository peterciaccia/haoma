"""
Created on 2021-09-21 by Peter Ciaccia
Contains common functions used for several test scripts, like reading and writing methods
"""

import os
import time
from functools import wraps
from pathlib import Path
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def get_log_path():
    """
    Writes logs for most files except tests
    :return:
    """
    log_dir = Path(os.getenv('PROJECT_LOG_DIR'))
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_name = Path(now)
    log_path = log_dir / log_name.with_suffix('.log')
    return log_path


logging.basicConfig(filename=get_log_path(),
                    filemode="w",
                    level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    # force=True
                    )
logger = logging.getLogger(__name__)


def timer(task, *args, **kwargs):
    """
    decorator function that times other functions
    :param task:
    :param args:
    :param kwargs:
    :return:
    """

    if logger.debug != logging.DEBUG:
        return task(*args, **kwargs)

    @wraps(task)
    def wrap(*args, **kwargs):
        start_time = time.time()
        task_complete = task(*args, **kwargs)
        end_time = time.time()
        logger.debug(f'task {task.__name__} args: {args} kwargs: {kwargs} '
                     f'took {end_time-start_time}.6f')
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
