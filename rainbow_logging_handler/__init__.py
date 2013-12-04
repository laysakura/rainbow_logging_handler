# -*- coding: utf-8 -*-
"""

    Python logging tuned to extreme.

"""
import logging
import os


class RainbowLoggingHandler(logging.StreamHandler):
    """ A colorful logging handler optimized for terminal debugging aestetichs.

    - Designed for diagnosis and debug mode output - not for disk logs

    - Highlight the content of logging message in more readable manner

    - Show function and line, so you can trace where your logging messages
      are coming from

    - Keep timestamp compact

    - Extra module/function output for traceability

    The class provide few options as member variables you
    would might want to customize after instiating the handler.
    """

    # [todo] - customizable color_map
    color_map = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'white': 7,
    }
    (csi, reset) = ('\x1b[', '\x1b[0m')

    # Define color for message payload
    level_map = {
        logging.DEBUG: (None, 'cyan', False),
        logging.INFO: (None, 'white', False),
        logging.WARNING: (None, 'yellow', True),
        logging.ERROR: (None, 'red', True),
        logging.CRITICAL: ('red', 'white', True),
    }

    date_format = "%H:%M:%S"

    #: How many characters reserve to function name logging
    who_padding = 22

    #: Show logger name
    show_name = True

    # Enable ANSI color code on Windows
    if os.name == 'nt':
        import colorama
        colorama.init()

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

        # Dynamic message color based on logging level
        if record.levelno in self.level_map:
            fg, bg, bold = self.level_map[record.levelno]
        else:
            # Defaults
            bg = None
            fg = "white"
            bold = False

        # Magician's hat
        # https://www.youtube.com/watch?v=1HRa4X07jdE
        template = [
            "[",
            self.get_color("black", None, True),
            "%(asctime)s",
            self.reset,
            "] ",
            self.get_color("white", None, True) if self.show_name else "",
            "%(name)s " if self.show_name else "",
            "%(padded_who)s",
            self.reset,
            " ",
            self.get_color(bg, fg, bold),
            "%(message)s",
            self.reset,
        ]

        format = "".join(template)

        who = [self.get_color("green"),
               getattr(record, "funcName", ""),
               "()",
               self.get_color("black", None, True),
               ":",
               self.get_color("cyan"),
               str(getattr(record, "lineno", 0))]

        who = "".join(who)

        # We need to calculate padding length manualy
        # as color codes mess up string length based calcs
        unformatted_who = getattr(record, "funcName", "") + "()" + \
            ":" + str(getattr(record, "lineno", 0))

        if len(unformatted_who) < self.who_padding:
            spaces = " " * (self.who_padding - len(unformatted_who))
        else:
            spaces = ""

        record.padded_who = who + spaces

        formatter = logging.Formatter(format, self.date_format)
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
        try:
            msg = self.format(record)
            msg = self._encode(msg)
            self.stream.write(msg + getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def _encode(self, msg):
        if unicode and isinstance(msg, unicode):
            enc = getattr(self.stream, 'encoding', 'utf-8')
            return msg.encode(enc, 'replace')
        return msg
