# -*- coding: utf-8 -*-
from nose.tools import *
import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler


def setup():
    logger = logging.getLogger('test_unicode')
    logger.setLevel(logging.DEBUG)
    handler = RainbowLoggingHandler(sys.stderr)
    logger.addHandler(handler)


def test_unicode():
    logger = logging.getLogger('test_unicode')
    logger.debug('日本語ログ')
    if (2, 6, 0) <= sys.version_info < (3, 0, 0):
        logger.debug(u'日本語ログ')
