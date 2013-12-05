# -*- coding: utf-8 -*-
from nose.tools import *
import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler


def setup():
    logger = logging.getLogger('test_logging')
    logger.setLevel(logging.DEBUG)
    handler = RainbowLoggingHandler(sys.stderr)
    logger.addHandler(handler)


def test_usage():
    logger = logging.getLogger('test_logging')

    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.error("error msg")
    logger.critical("critical msg")

    try:
        raise RuntimeError("Opa!")
    except Exception as e:
        logger.exception(e)


def test_custom_format():
    logger = logging.getLogger('test_logging_custom_format')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("MESSAGE ONLY => %(message)s")

    handler = RainbowLoggingHandler(sys.stderr)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.error("error msg")
    logger.critical("critical msg")


def test_custom_color():
    logger = logging.getLogger('test_logging_custom_color')
    logger.setLevel(logging.DEBUG)

    handler = RainbowLoggingHandler(
        sys.stderr,
        color_asctime       = ('black', 'white', True),
        color_name          = ('black', 'white', True),
        color_message_debug = ('black', 'white', True),
    )
    logger.addHandler(handler)

    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.error("error msg")
    logger.critical("critical msg")


def test_format_all_column():
    logger = logging.getLogger('test_logging_format_all_column')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('''
        name            = '%(name)s'
        levelno         = '%(levelno)s'
        levelname       = '%(levelname)s'
        pathname        = '%(pathname)s'
        filename        = '%(filename)s'
        module          = '%(module)s'
        lineno          = '%(lineno)d'
        funcName        = '%(funcName)s'
        created         = '%(created)f'
        asctime         = '%(asctime)s'
        msecs           = '%(msecs)d'
        relativeCreated = '%(relativeCreated)d'
        thread          = '%(thread)d'
        threadName      = '%(threadName)s'
        process         = '%(process)d'
        message         = '%(message)s'
    ''')

    handler = RainbowLoggingHandler(sys.stderr)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug("debug msg")
