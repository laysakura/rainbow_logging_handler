# -*- coding: utf-8 -*-
"""

    Python logging tuned to extreme.

"""
import logging
import os


class RainbowLoggingHandler(logging.StreamHandler):
    """ A colorful logging handler optimized for terminal debugging aesthetics.

    - Designed for diagnosis and debug mode output - not for disk logs

    - Highlight the content of logging message in more readable manner

    - Show function and line, so you can trace where your logging messages
      are coming from

    - Keep timestamp compact

    - Extra module/function output for traceability

    The class provide few options as member variables you
    would might want to customize after instiating the handler.
    """

    color_map = {
        'black'   : 0,
        'red'     : 1,
        'green'   : 2,
        'yellow'  : 3,
        'blue'    : 4,
        'magenta' : 5,
        'cyan'    : 6,
        'white'   : 7,
    }
    (csi, reset) = ('\x1b[', '\x1b[0m')

    #: Show logger name
    show_name = True

    #: (Default) format string, w/o color code
    _fmt = '[%(asctime)s] %(name)s %(funcName)s():%(lineno)d\t%(message)s'

    #: Color of each column
    _column_color = {
        # '%(asctime)s' : ("black", None, True),
        # ...
        '%(message)s' : {
            # logging.DEBUG   : ('cyan'  , None , False),
            # ...
        },
    }

    # Enable ANSI color code on Windows
    if os.name == 'nt':
        import colorama
        colorama.init()

    def __init__(
        self, stream,

        datefmt='%H:%M:%S',

        color_name             = ('white' , None, True),
        color_levelno          = ('white' , None, False),
        color_levelname        = ('white' , None, True),
        color_pathname         = ('blue'  , None, True),
        color_filename         = ('blue'  , None, True),
        color_module           = ('yellow', None, True),
        color_lineno           = ('cyan'  , None, True),
        color_funcName         = ('green' , None, False),
        color_created          = ('white' , None, False),
        color_asctime          = ('black' , None, True),
        color_msecs            = ('white' , None, False),
        color_relativeCreated  = ('white' , None, False),
        color_thread           = ('white' , None, False),
        color_threadName       = ('white' , None, False),
        color_process          = ('white' , None, False),

        color_message_debug    = ('cyan'  , None , False),
        color_message_info     = ('white' , None , False),
        color_message_warning  = ('yellow', None , True),
        color_message_error    = ('red'   , None , True),
        color_message_critical = ('white' , 'red', True),
    ):
        """Construct colorful stream handler

        :param stream:  a stream to emit log (e.g. sys.stderr, sys.stdout, writable `file` object, ...)
        :type color_*:  str compatible to `time.strftime()` argument
        :param datefmt: format of %(asctime)s, passed to `logging.Formatter.__init__()`.
            If `None` is passed, `logging`'s default format of '%H:%M:%S,<milliseconds>' is used.
        :type color_*:  `(<symbolic name of foreground color>, <symbolic name of background color>, <brightness flag>)`
        :param color_*: Each column's color. See `logging.Formatter` for supported column (`*`)
        """
        logging.StreamHandler.__init__(self, stream)

        # set timestamp format
        self._datefmt = datefmt

        # set custom color
        self._column_color['%(name)s']            = color_name
        self._column_color['%(levelno)s']         = color_levelno
        self._column_color['%(levelname)s']       = color_levelname
        self._column_color['%(pathname)s']        = color_pathname
        self._column_color['%(filename)s']        = color_filename
        self._column_color['%(module)s']          = color_module
        self._column_color['%(lineno)d']          = color_lineno
        self._column_color['%(funcName)s']        = color_funcName
        self._column_color['%(created)f']         = color_created
        self._column_color['%(asctime)s']         = color_asctime
        self._column_color['%(msecs)d']           = color_msecs
        self._column_color['%(relativeCreated)d'] = color_relativeCreated
        self._column_color['%(thread)d']          = color_thread
        self._column_color['%(threadName)s']      = color_threadName
        self._column_color['%(process)d']         = color_process
        self._column_color['%(message)s'][logging.DEBUG]    = color_message_debug
        self._column_color['%(message)s'][logging.INFO]     = color_message_info
        self._column_color['%(message)s'][logging.WARNING]  = color_message_warning
        self._column_color['%(message)s'][logging.ERROR]    = color_message_error
        self._column_color['%(message)s'][logging.CRITICAL] = color_message_critical

    @property
    def is_tty(self):
        """Returns true if the handler's stream is a terminal."""
        return getattr(self.stream, 'isatty', lambda: False)()

    def get_color(self, fg=None, bg=None, bold=False):
        """
        Construct a terminal color code

        :param fg: Symbolic name of foreground color

        :param bg: Symbolic name of background color

        :param bold: Brightness bit
        """
        params = []
        if bg in self.color_map:
            params.append(str(self.color_map[bg] + 40))
        if fg in self.color_map:
            params.append(str(self.color_map[fg] + 30))
        if bold:
            params.append('1')

        color_code = ''.join((self.csi, ';'.join(params), 'm'))

        return color_code

    def colorize(self, record):
        """
        Get a special format string with ASCII color codes.
        """
        color_fmt = self._colorize_fmt(self._fmt, record.levelno)
        formatter = logging.Formatter(color_fmt, self._datefmt)
        self.colorize_traceback(formatter, record)
        output = formatter.format(record)
        # Clean cache so the color codes of traceback don't leak to other formatters
        record.ext_text = None
        return output

    def colorize_traceback(self, formatter, record):
        """
        Turn traceback text to red.
        """
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            record.exc_text = "".join([
                self.get_color("red"),
                formatter.formatException(record.exc_info),
                self.reset,
            ])

    def format(self, record):
        """
        Formats a record for output.

        Takes a custom formatting path on a terminal.
        """
        if self.is_tty:
            message = self.colorize(record)
        else:
            message = logging.StreamHandler.format(self, record)

        return message

    def emit(self, record):
        """Emit colorized `record` when called from `logging` module's printing functions"""
        try:
            msg = self.format(record)
            msg = self._encode(msg)
            self.stream.write(msg + getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def setFormatter(self, formatter):
        # HACK: peeping format string passed by user to `logging.Formatter()`
        if formatter._fmt:
            self._fmt = formatter._fmt
        logging.StreamHandler.setFormatter(self, formatter)

    def _encode(self, msg):
        """Encode `msg` if it is `unicode` object"""
        import sys
        if (2, 6, 0) <= sys.version_info < (3, 0, 0) and unicode and isinstance(msg, unicode):
            enc = getattr(self.stream, 'encoding', 'utf-8')
            if enc is None:
                # An encoding property was found, but it was None
                enc = 'utf-8'
            return msg.encode(enc, 'replace')
        return msg

    def _colorize_fmt(self, fmt, levelno):
        """Adds ANSI color codes on plain `fmt`"""
        for column in self._column_color.keys():
            pos = fmt.find(column)
            if pos == -1:
                continue
            (pre_col, post_col) = (fmt[:pos], fmt[pos + len(column):])
            color_tup = self._column_color[column] if column != '%(message)s' else self._column_color[column][levelno]
            fmt = ''.join([pre_col,
                           self.reset, self.get_color(*color_tup), column, self.reset,
                           post_col])
        return fmt
