"""

"""
# built-ins
import os
from datetime import datetime
from pathlib import Path
import logging
import logging.config

# dependencies
from dotenv import load_dotenv

# in-app
# nothing

load_dotenv()


def get_log_path(path=None):
    """
    Writes logs for most files except tests
    :param path:
    :return:
    """
    if path is None:
        log_dir = os.path.join(os.getenv("PROJECT_DIR"), "logs", "dated")
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_name = Path(now)
    elif path == "latest":
        log_dir = os.path.join(os.getenv("PROJECT_DIR"), "logs")
        log_name = Path("latest")
    else:
        raise SyntaxError
    log_path = os.path.join(log_dir, log_name.with_suffix(".log"))
    return log_path


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s, %(levelname)-2s [%(name)s] %(module)s %(lineno)d:  %(message)s'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': get_log_path(),
            'mode': 'a',
            'encoding': 'utf-8'
        },
        'recent': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': get_log_path(path="latest"),
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True
        },
        'test': {
            'handlers': ['file', 'recent'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def resolve_class_namespace(cls):
    """Resolves namespace for logger"""
    return f"{cls.__module__}.{cls.__qualname__}"


def get_logger(*args, module=None, cls=None):
    """Prepares logger for given class or module """
    if '__main__' in args:
        logger = logging.getLogger(__name__)
    if module is not None and cls is not None:
        raise ValueError('cannot pass module names and class declarations simultaneously')
    elif module is not None:
        logger = logging.getLogger(module)
    elif cls is not None:
        logger = logging.getLogger(resolve_class_namespace(cls))
    elif cls is None and module is None:
        logger = logging.getLogger()
        logger.debug('logger set to default root logger')
    else:
        raise SyntaxError

    return logger
