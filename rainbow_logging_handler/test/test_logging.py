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
