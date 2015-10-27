from pony import orm

import db


def list_all():
    list_projects()
    list_tasks()
    list_ideas()
    list_reminders()
    show_scratchpad()


def list_reminders():
    reminders = db.Reminder.select().order_by(db.Reminder.when)
    _list_simple_objects(reminders, 'reminders')


def list_ideas():
    ideas = db.Idea.select()
    _list_simple_objects(ideas, 'ideas')


def list_tasks():
    tasks = orm.select(task for task in db.Task if task.project is None)
    _list_simple_objects(tasks, 'tasks')


def list_project(project):
    print(project.name.upper())
    print('-' * len(project.name))
    for task in project.tasks:
        print(task)
    print()


def show_scratchpad():
    scratchpad_content = db.get_scratchpad_content()
    if scratchpad_content:
        print('SCRATCHPAD')
        print('----------')
        print(scratchpad_content)


def list_projects():
    for project in db.Project.select():
        list_project(project)


def _list_simple_objects(objects, title):
    """Print title separated from newlined objects."""

    if not objects:
        return

    print(title.upper())
    print('-' * len(title))
    for object in objects:
        print(object)
    print()
