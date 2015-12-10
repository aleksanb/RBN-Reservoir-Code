import pickle
import logging
from datetime import datetime

logger = logging.getLogger()

def confirm(message):
    return raw_input(message + ' [y/N] ').strip() == 'y'


def default_input(name, default):
    return int(raw_input('{} ({}): '.format(name, default))
               or default)

def load(query, pickle_dir='pickle_dumps/'):
    name = pickle_dumps + raw_input(query + ' ')
    obj = pickle.load(open(name, 'r'))

    logger.info('Loaded pickle: {}'.format(name))

    return obj

def dump(obj, name, folder=None, pickle_dir='pickle_dumps/'):
    if folder:
        pickle_dir = pickle_dir + folder + '/'

    date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    name = '{}{}-{}'.format(pickle_dir, date, name)

    pickle.dump(obj, open(name, 'w'))
    logger.info('Created pickle: {}'.format(name))
