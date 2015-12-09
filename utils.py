def confirm(message):
    return raw_input(message + ' [y/N] ').strip() == 'y'


def default_input(name, default):
    return int(raw_input('{} ({}): '.format(name, default))
               or default)
