"""

"""

import logging
import logging.config
import log.conf


CONFIG = {'level': 'DEBUG',
          'quiet': False,
          'propagate': True
          }


def get_root():
    """Returns the module root"""
    return 'Haoma'


def resolve_class_namespace(cls):
    """Resolves namespace for logger"""
    return f"{cls.__module__}.{cls.__qualname__}"


def get_logger(module=None, cls=None):
    """Prepares logger for given class or module """
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

    logger.propagate = CONFIG['propagate']
    if CONFIG['quiet'] is True:
        logger.addHandler(logging.NullHandler())
        return logger
    # logging.config.dictConfig(log.conf.default_config)
    logger.setLevel(CONFIG['level'])
    return logger
