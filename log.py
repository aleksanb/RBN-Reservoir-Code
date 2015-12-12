import logging
from termcolor import colored
import arrow
import os


class BaseFormatter(logging.Formatter):

    def get_time(self, record):
        return arrow.get(record.created).isoformat()

    def get_level(self, record):
        return record.levelname

    def get_location(self, record):
        return '%s:%s' % (os.path.relpath(record.pathname), record.lineno)

    def get_message(self, record):
        return record.message

    def format(self, record):
        super(BaseFormatter, self).format(record)
        return ' - '.join((self.get_time(record),
                           self.get_level(record),
                           self.get_location(record),
                           self.get_message(record)))


class ColoredFormatter(BaseFormatter):
    level_colors = {
        'CRITICAL': 'white',
        'ERROR': 'red',
        'WARNING': 'yellow',
        'INFO': 'cyan',
        'DEBUG': 'green',
    }

    level_bg_colors = {
        'CRITICAL': 'red',
        'ERROR': 'grey',
        'WARNING': 'grey',
        'INFO': 'grey',
        'DEBUG': 'grey',
    }

    def get_time(self, record):
        return colored(super(ColoredFormatter, self).get_time(record),
                       'white',
                       attrs=['dark'])

    def get_level(self, record):
        return colored(super(ColoredFormatter, self).get_level(record),
                       self.level_colors[record.levelname],
                       'on_' + self.level_bg_colors[record.levelname])

    def get_location(self, record):
        return colored(super(ColoredFormatter, self).get_location(record),
                       'white',
                       attrs=['dark'])

    def get_message(self, record):
        return colored(super(ColoredFormatter, self).get_message(record),
                       'white')


def setup(level, name='', path=''):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    name = (name or 'out') + '.log'
    if path:
        name = path + name

    handler = logging.FileHandler(name)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(BaseFormatter())

    logger.addHandler(handler)

    if level <= logging.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)
