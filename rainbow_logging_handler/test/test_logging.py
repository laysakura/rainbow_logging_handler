# -*- coding: utf-8 -*-
from nose.tools import *
import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler


def test_usage():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    handler = RainbowLoggingHandler(sys.stderr)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    logger = logging.getLogger('test')

    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.error("error msg")
    logger.critical("critical msg")

    try:
        raise RuntimeError("Opa!")
    except Exception as e:
        logger.exception(e)
