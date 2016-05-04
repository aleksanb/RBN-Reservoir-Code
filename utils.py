import pickle
import logging
import os
import subprocess
import glob
from datetime import datetime
import numpy as np

logger = logging.getLogger()


def select(field, collection):
    return [item[field] for item in collection]


def fst(t):
    return t[0]


def snd(t):
    return t[1]


def lst(t):
    return t[-1]


def user_denies(message):
    return raw_input(message + ' [Y/n] ').strip() == 'n'


def user_confirms(message):
    return raw_input(message + ' [N/y] ').strip() == 'y'


def deviation_stats(description, numbers):
    logger.info('Stats for {} ({} items)'.format(description, len(numbers)))
    logger.info(
        'Largest: {}, Smallest: {}, Mean: {}, Std: {}'
        .format(max(numbers), min(numbers), np.mean(numbers), np.std(numbers)))


def default_input(name, default):
    query = raw_input('{} (default: {}): '.format(name, default))

    if query:
        if type(default) is int:
            return int(query)
        elif type(default) is str:
            return str(query)
        elif type(default) is float:
            return float(query)

    return default


def get_working_dir(prefix='pickle_dumps'):
    directory = default_input('Set working directory', '')

    working_dir = '{}/{}/'.format(prefix, directory)
    if not os.path.exists(working_dir):
        if not user_denies('Directory {} does not exist. Create it?'
                           .format(working_dir)):
            os.makedirs(working_dir)
            logger.info('Created folder: {}'.format(working_dir))

    return working_dir


def glob_load(pattern):
    matches = glob.glob(pattern)

    if len(matches) == 0:
        logger.warn(
            'No files matching pattern {}!'.format(pattern))
        return None

    results = [(pickle.load(open(match, 'r')), match)
               for match in matches]

    logger.info('Loaded {} pickle(s): {}'.format(
        len(matches),
        matches))

    return results


def load(query, folder=''):
    name = folder + raw_input(
        '{} (from {}) '.format(query, folder))
    obj = pickle.load(open(name, 'r'))

    logger.info('Loaded pickle: {}'.format(name))

    return obj


def dump(obj, name, folder=''):
    date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    name = '{}{}-{}'.format(folder, date, name)

    pickle.dump(obj, open(name, 'w'))
    logger.info('Created pickle: {}'.format(name))


def git(*args):
    gitproc = subprocess.Popen(['git'] + list(args), stdout=subprocess.PIPE)
    stdout, _ = gitproc.communicate()
    return stdout.strip()


def log_git_info():
    logger.info('git revision: %s' % git('rev-parse', 'HEAD'))
    if git('diff'):
        logger.warn('Git working directory not clean!')
