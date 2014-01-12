#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name             = 'rainbow_logging_handler',
    description      = 'Ultimate Python colorized logger with user-custom color',
    long_description = open('README.rst').read(),
    url              = 'https://github.com/laysakura/rainbow_logging_handler',
    license          = 'LICENSE.txt',
    version          = '2.2.0',
    author           = 'Mikko Ohtamaa, Sho Nakatani',
    author_email     = 'mikko@opensourcehacker.com, lay.sakura@gmail.com',
    install_requires = [
        'logutils',
        'colorama',
    ],
    tests_require    = [
        'nose',
        'coverage',
        'nose-cov',
    ],
    packages         = [
        'rainbow_logging_handler',
        'rainbow_logging_handler.test',
    ],
    scripts          = [
    ],
    classifiers      = '''
Programming Language :: Python
Development Status :: 5 - Production/Stable
License :: Public Domain
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: Implementation :: PyPy
Operating System :: POSIX :: Linux
Operating System :: POSIX :: BSD
Operating System :: Unix
Operating System :: MacOS
Operating System :: Microsoft :: Windows
Intended Audience :: Developers
Topic :: Software Development :: Debuggers
Topic :: System :: Logging
Topic :: Terminals
Topic :: Utilities
'''.strip().splitlines()
)
