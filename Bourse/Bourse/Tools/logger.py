# -*- coding: utf-8 -*-
import logging
import sys
import os


def loggers(log_level='debug'):
    filename = '[{}]'.format(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:])
    logger = logging.getLogger(filename)
    if log_level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'warn':
        logger.setLevel(logging.WARN)
    elif log_level == 'error':
        logger.setLevel(logging.ERROR)
    elif log_level == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger


class logger(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = loggers()
        return cls._instance

