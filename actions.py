from collections import namedtuple
from exceptions import QuitException

from pony import orm

import db
import ui

Action = namedtuple('Action', ('mnemonic', 'name', 'run'))


def action(mnemonic, name):
    return lambda run: Action(mnemonic, name, run)


@action('q', 'Quit')
def quit():
    raise QuitException()


@action('i', 'New long-term idea')
@orm.db_session
def new_idea():
    content = ui.ask('Tell me all about it.')
    db.Idea(content=content)


@action('t', 'New task')
@orm.db_session
def new_task():
    content = ui.ask('What do you want to have done?')
    db.Task(content=content)


@action('s', 'Open scratchpad')
@orm.db_session
def open_scratchpad():
    scratchpad = db.get_scratchpad()
    new_content = ui.ask_from_editor(scratchpad.content)
    scratchpad.content = new_content


@action('l', 'List tasks and ideas')
@orm.db_session
def list_all():
    if len(db.Task.select()):
        print('TASKS')
        for task in db.Task.select():
            print(task)
        print()

    if len(db.Idea.select()):
        print('IDEAS')
        for idea in db.Idea.select():
            print(idea)


MAIN_ACTIONS = [new_task, new_idea, open_scratchpad, list_all, quit]
