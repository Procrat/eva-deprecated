from collections import namedtuple
import ui

import exceptions


Action = namedtuple('Action', ('mnemonic', 'name', 'run'))


def action(mnemonic, name):
    return lambda run: Action(mnemonic, name, run)


@action('q', 'Quit')
def quit():
    raise exceptions.QuitException()


@action('i', 'New long-term idea')
def new_idea():
    idea = ui.ask('Tell me all about it.')
    # TODO save idea


@action('t', 'New task')
def new_task():
    task = ui.ask('What do you want to have done?')
    # TODO save task


MAIN_ACTIONS = [new_task, new_idea, quit]
