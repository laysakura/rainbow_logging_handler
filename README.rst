rainbow_logging_handler
=======================
.. image:: https://travis-ci.org/laysakura/rainbow_logging_handler.png?branch=master
   :target: https://travis-ci.org/laysakura/rainbow_logging_handler

Ultimate Python colorized logger.

Usage
-----

.. image:: http://github.com/laysakura/rainbow_logging_handler/raw/master/doc/screenshot.png

This script runs like above screenshot.

.. code-block:: python

    import sys
    import logging
    from rainbow_logging_handler import RainbowLoggingHandler

    if __name__ == '__main__':
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


Install
-------

Install from PyPI
#################
.. code-block:: bash

    $ pip install nextversion

Install from Github repo
########################
.. code-block:: bash

    $ git clone https://github.com/laysakura/rainbow_logging_handler.git
    $ cd rainbow_logging_handler
    $ ./setup.py install

Author
======

Mikko Ohtamaa <mikko@opensourcehacker.com>, Sho Nakatani <lay.sakura@gmail.com>

License
-------

This is free and unencumbered public domain software. For more information,
see <http://unlicense.org/> or the accompanying `LICENSE.txt` file.
