from collections import namedtuple

from pony.orm import db_session

from exceptions import QuitException
from db import Idea, Task
import ui


Action = namedtuple('Action', ('mnemonic', 'name', 'run'))


def action(mnemonic, name):
    return lambda run: Action(mnemonic, name, run)


@action('q', 'Quit')
def quit():
    raise QuitException()


@action('i', 'New long-term idea')
@db_session
def new_idea():
    content = ui.ask('Tell me all about it.')
    Idea(content=content)


@action('t', 'New task')
@db_session
def new_task():
    content = ui.ask('What do you want to have done?')
    Task(content=content)


@action('l', 'List tasks and ideas')
@db_session
def list_all():
    if len(Task.select()):
        print('TASKS')
        for task in Task.select():
            print(task)
        print()

    if len(Idea.select()):
        print('IDEAS')
        for idea in Idea.select():
            print(idea)


MAIN_ACTIONS = [new_task, new_idea, list_all, quit]
