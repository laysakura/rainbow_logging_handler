rainbow_logging_handler
=======================
.. image:: https://travis-ci.org/laysakura/rainbow_logging_handler.png?branch=master
   :target: https://travis-ci.org/laysakura/rainbow_logging_handler

.. image:: https://pypip.in/v/rainbow_logging_handler/badge.png
    :target: https://pypi.python.org/pypi/rainbow_logging_handler
    :alt: Latest PyPI version

Ultimate Python colorized logger.

.. contents:: :local:

Usage
-----

Generic usage example
#####################
.. image:: http://github.com/laysakura/rainbow_logging_handler/raw/master/doc/screenshot.png

This script runs like above screenshot.

.. code-block:: python

    import sys
    import logging
    from rainbow_logging_handler import RainbowLoggingHandler

    def main_func():
        # setup `logging` module
        logger = logging.getLogger('test_logging')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s")  # same as default

        # setup `RainbowLoggingHandler`
        handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.debug("debug msg")
        logger.info("info msg")
        logger.warn("warn msg")
        logger.error("error msg")
        logger.critical("critical msg")

        try:
            raise RuntimeError("Opa!")
        except Exception as e:
            logger.exception(e)

    if __name__ == '__main__':
        main_func()


Usage with Django
##################################

.. image:: http://github.com/miohtama/rainbow_logging_handler/raw/master/doc/screenshot_django.png

`Django <https://www.djangoproject.com/>`_ is a popular Python web framework.

Put the following to your ``settings.py`` to get more pleasant development server console output::

    # Add this to your settings.py
    if DEBUG:
        # Install rainbow logging handler when running Django in develoment mode
        import sys
        LOGGING["handlers"]["rainbow"] = {"level": "DEBUG", "class": "rainbow_logging_handler.RainbowLoggingHandler", 'stream': sys.stderr}
        LOGGING["loggers"]['']["handlers"].append("rainbow")

`More about configuring loggers for Django <https://docs.djangoproject.com/en/dev/topics/logging/>`_.


Usage with Pyramid
#######################

Set ``handler_console`` section in ``develop.ini``:

   [handler_console]
   class = rainbow_logging_handler.RainbowLoggingHandler
   args = (sys.stderr,)
   level = NOTSET
   format = [%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s

Features
--------

Column-by-column colored log
############################
As apparent from above screenshot, each column of logs are differently colored.
Even default coloring should make log reading easier.

User custom color
#################
Every column colors are **customizable**.

.. code-block:: python

    formatter = logging.Formatter('%(pathname)s [%(module)s] - %(funcName)s:L%(lineno)d : %(message)s')
    handler   = RainbowLoggingHandler(
        sys.stderr,
        # Customizing each column's color
        color_pathname=('black', 'red'  , True), color_module=('yellow', None, False),
        color_funcName=('blue' , 'white', True), color_lineno=('green' , None, False),
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("hello custom world")

Above code produces output like this.

.. image:: http://github.com/laysakura/rainbow_logging_handler/raw/master/doc/screenshot-custom-color.png

High portability
################
Linux, BSD, Mac OS, and Windows are supposed to be supported.

Runs with both Python 2.6 or higher & Python 3.2 or higher.

Install
-------

Install from PyPI
#################
.. code-block:: bash

    $ pip install rainbow_logging_handler

Install from Github repo
########################
.. code-block:: bash

    $ git clone https://github.com/laysakura/rainbow_logging_handler.git
    $ cd rainbow_logging_handler
    $ ./setup.py install

Author
------

Mikko Ohtamaa <mikko@opensourcehacker.com>, Sho Nakatani <lay.sakura@gmail.com>

And special thanks to `10sr <https://github.com/10sr>`_ for advice.

License
-------

This is free and unencumbered public domain software. For more information,
see <http://unlicense.org/> or the accompanying `LICENSE.txt` file.
