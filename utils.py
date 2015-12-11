import pickle
import logging
import os
from datetime import datetime

logger = logging.getLogger()


def user_denies(message):
    return raw_input(message + ' [Y/n] ').strip() == 'n'


def user_confirms(message):
    return raw_input(message + ' [N/y] ').strip() == 'y'


def default_input(name, default):
    query = raw_input('{} (default: {}): '.format(name, default))

    if query:
        if type(default) is int:
            return int(query)
        elif type(default) is str:
            return str(query)

    return default


def load(query, folder=None, pickle_dir='pickle_dumps/'):
    if folder:
        pickle_dir = pickle_dir + folder + '/'

    name = pickle_dir + raw_input(
        '{} (from {}) '.format(query, pickle_dir))
    obj = pickle.load(open(name, 'r'))

    logger.info('Loaded pickle: {}'.format(name))

    return obj


def dump(obj, name, folder=None, pickle_dir='pickle_dumps/'):
    if folder:
        pickle_dir = pickle_dir + folder + '/'

    if not os.path.exists(pickle_dir):
        os.makedirs(pickle_dir)

    date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    name = '{}{}-{}'.format(pickle_dir, date, name)

    pickle.dump(obj, open(name, 'w'))
    logger.info('Created pickle: {}'.format(name))
