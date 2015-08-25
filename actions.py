from exceptions import QuitException

from pony import orm

import db
import ui


def Action(mnemonic: str, name: str):
    return lambda run: ui.Choice(mnemonic, name, run)


@Action('q', 'Quit')
def quit():
    raise QuitException()


@Action('i', 'New long-term idea')
@orm.db_session
def new_idea():
    content = ui.ask('Tell me all about it.')
    db.Idea(content=content)


@Action('p', 'New project')
@orm.db_session
def new_project():
    name = ui.ask('What project are you planning on taking on?')
    db.Project(name=name)


@Action('t', 'New task')
@orm.db_session
def new_task():
    content = ui.ask('What do you want to have done?')
    project_choices = list(_generate_project_choices())
    project = ui.let_choose('Is it part of a project?', project_choices,
                            none_option='No')
    db.Task(content=content, project=project)


@Action('s', 'Open scratchpad')
@orm.db_session
def open_scratchpad():
    scratchpad = db.get_scratchpad()
    new_content = ui.ask_from_editor(scratchpad.content)
    scratchpad.content = new_content


@Action('l', 'List everything')
@orm.db_session
def list_all():
    for project in db.Project.select():
        print(project.name.upper())
        print('-' * len(project.name))
        for task in project.tasks:
            print(task)
        print()

    # List tasks that aren't part of a project
    tasks = orm.select(task for task in db.Task if task.project is None)
    if tasks:
        print('TASKS')
        print('-----')
        for task in tasks:
            print(task)
        print()

    ideas = db.Idea.select()
    if ideas:
        print('IDEAS')
        print('-----')
        for idea in ideas:
            print(idea)


def _generate_project_choices():
    mnemonics = {}
    no_mnemonic_possible_counter = 0

    for project in db.Project.select():
        for letter in project.name.lower():
            if letter not in mnemonics:
                break
        else:
            letter = str(no_mnemonic_possible_counter)
            no_mnemonic_possible_counter += 1

        yield ui.Choice(letter, project.name, project)


MAIN_ACTIONS = [
    new_task,
    new_project,
    new_idea,
    open_scratchpad,
    list_all,
    quit,
]
