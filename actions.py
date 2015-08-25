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


@action('p', 'New project')
@orm.db_session
def new_project():
    name = ui.ask('What project are you planning on taking on?')
    db.Project(name=name)


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


@action('l', 'List everything')
@orm.db_session
def list_all():
    for project in db.Project.select():
        print(project.name.upper())
        print('-' * len(project.name))
        for task in project.tasks:
            print(task)
        print()

    if len(db.Task.select()):
        print('TASKS')
        print('-----')
        for task in db.Task.select():
            print(task)
        print()

    if len(db.Idea.select()):
        print('IDEAS')
        print('-----')
        for idea in db.Idea.select():
            print(idea)


MAIN_ACTIONS = [
    new_task,
    new_project,
    new_idea,
    open_scratchpad,
    list_all,
    quit,
]
