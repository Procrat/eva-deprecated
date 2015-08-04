from collections import namedtuple

import exceptions


Action = namedtuple('Action', ('mnemonic', 'name', 'run'))


def action(mnemonic, name):
    return lambda run: Action(mnemonic, name, run)


@action('q', 'Quit')
def quit():
    raise exceptions.QuitException()


@action('s', 'Do something')
def something():
    print('Cool.')


MAIN_ACTIONS = [something, quit]
