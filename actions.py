from exceptions import QuitException

from pony import orm

import db
import ui
import notifier


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
    project = db.Project(name=name)

    # Ask for tasks in this project
    while True:
        task = ui.ask('What does this project consist of?')
        if not task:
            break
        db.Task(content=task, project=project)


@Action('r', 'New reminder')
@orm.db_session
def new_reminder():
    content = ui.ask('What do you want me to remind you of?')
    if not content:
        return
    when = ui.pick_date('When do you want to be reminded?',
                        'You will be reminded at {}.')
    if not when:
        question = "Are you sure you don't want to be reminded?"
        if ui.ask_polar_question(question):
            return
    reminder = db.Reminder(content=content, when=when)
    notifier.delayed_notify(reminder)


@Action('t', 'New task')
@orm.db_session
def new_task():
    content = ui.ask('What do you want to have done?')

    if ui.ask_polar_question('Does it take less than two minutes?'):
        print("Do it now! I'll wait.")
        input('> ')
        return

    task = db.Task(content=content)

    project_choices = list(_generate_project_choices())
    task.project = ui.let_choose('Is it part of a project?', project_choices,
                                 none_option='No')

    if ui.ask_polar_question('Can it be devided in smaller chunks?'):
        while True:
            subtask_content = ui.ask('Like what?')
            if not subtask_content:
                break
            subtask = db.Task(content=subtask_content, project=task.project)
            task.subtasks.add(subtask)


@Action('s', 'Open scratchpad')
@orm.db_session
def open_scratchpad():
    scratchpad = db.get_scratchpad()
    new_content = ui.ask_from_editor(scratchpad.content)
    scratchpad.content = new_content


@Action('l', 'List everything')
@orm.db_session
def list_all():
    def _list_simple_objects(objects, title):
        if not objects:
            return

        print(title.upper())
        print('-' * len(title))
        for object in objects:
            print(object)
        print()

    for project in db.Project.select():
        print(project.name.upper())
        print('-' * len(project.name))
        for task in project.tasks:
            print(task)
        print()

    # List tasks that aren't part of a project
    tasks = orm.select(task for task in db.Task if task.project is None)
    _list_simple_objects(tasks, 'tasks')

    ideas = db.Idea.select()
    _list_simple_objects(ideas, 'ideas')

    reminders = db.Reminder.select().order_by(db.Reminder.when)
    _list_simple_objects(reminders, 'reminders')

    scratchpad = db.get_scratchpad()
    if scratchpad.content:
        print('SCRATCHPAD')
        print('----------')
        print(scratchpad.content)


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
    new_reminder,
    open_scratchpad,
    list_all,
    quit,
]
