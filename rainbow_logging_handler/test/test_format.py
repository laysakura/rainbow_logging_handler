# -*- coding: utf-8 -*-
from nose.tools import *
from tempfile import mkstemp
import os
import logging
from rainbow_logging_handler import RainbowLoggingHandler


(f_log, logpath) = (None, None)


def setup():
    # prepare log file
    global f_log, logpath
    (fd, logpath) = mkstemp(prefix='raibow-', suffix='.txt')
    f_log = os.fdopen(fd, 'w')

    # prepare 'test_format' logger
    logger = logging.getLogger('test_format')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("AAA %(name)s - %(levelname)s - %(message)s ZZZ")  # testing whether this format is used

    handler = RainbowLoggingHandler(f_log)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def teardown():
    # destroy log file
    global f_log, logpath
    f_log.close()
    os.remove(logpath)


def test_format_correctness():
    logger = logging.getLogger('test_format')
    logger.critical("critical msg")

    global logpath
    with open(logpath, 'r') as f:
        eq_(f.read(), 'AAA test_format - CRITICAL - critical msg ZZZ%s' % (os.linesep))
