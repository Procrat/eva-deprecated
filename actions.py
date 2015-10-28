import re

from pony import orm

import db
from exceptions import QuitException
import notifier
import ui
import utils


def Action(mnemonic: str, name: str):
    return lambda run: ui.Choice(mnemonic, name, run)


@Action('q', 'Quit')
def quit():
    raise QuitException()


@Action('w', "I don't know. What should I do, Eva?")
@orm.db_session
def what_now():
    task = _most_urgent() or _most_important()

    if not task:
        print("You're all done! Why don't you take a break? ^_^")
        print("If you really don't have anything to do, maybe you can take a"
              " look at your idea list?")
        return

    print('I suggest that you {}'.format(task.content))
    if ui.ask_polar_question('Do you wanna do this?'):
        ui.ask("Tell me when you're finished or if you're stopping.")

        if ui.ask_polar_question('Is it done?'):
            print('Good job! ^_^')
            task.delete()
    else:
        @Action('w', "I'm waiting for something.")
        def waiting_for():
            task.waiting_for = ui.ask('What are you waiting for?')
            print('All right, noted. If you need to poke someone for this or'
                  ' if you can easily speed this up, do it now.')

        reason = ui.let_choose('Why not?', [waiting_for], none_option='Meh')
        if reason is not None:
            reason()


@Action('i', 'New long-term idea')
@orm.db_session
def new_idea():
    content = ui.ask('Tell me all about it.')
    db.Idea(content=content)


@Action('p', 'New project')
@orm.db_session
def new_project():
    while True:
        name = ui.ask('What project are you planning on taking on?')
        if not name:
            return

        if orm.exists(project for project in db.Project
                      if project.name == name):
            ui.show('A project with this name already exists. '
                    'Please choose another name or leave empty to exit.')
        else:
            break

    project = db.Project(name=name)

    project.deadline = _ask_deadline()

    project.importance = _ask_importance()

    ui.show("If you're finished just say 'ready' :)")
    # Ask for tasks in this project
    while True:
        task = ui.ask('What does this project consist of?')
        if re.match("^|[rR]eady", task) is not None:
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
        ui.ask("Do it now! I'll wait.")
        return

    task = db.Task(content=content)

    project_choices = list(_generate_project_choices())
    if project_choices:
        task.project = ui.let_choose('Is it part of a project?',
                                     project_choices, none_option='No')

    task.deadline = _ask_deadline()

    task.importance = _ask_importance()

    task.duration = _ask_duration()

    if task.is_urgent() and not task.is_important():
        task.waiting_for = _ask_delegation()

    if ui.ask_polar_question('Can it be divided in smaller chunks?'):
        while True:
            subtask_content = ui.ask('Like what?')
            if not subtask_content:
                break
            subtask = db.Task(content=subtask_content, project=task.project)
            subtask.duration = _ask_duration()
            task.subtasks.add(subtask)


@Action('s', 'Open scratchpad')
def open_scratchpad():
    old_content = db.get_scratchpad_content()
    new_content = ui.ask_from_editor(old_content)
    db.set_scratchpad_content(new_content)


@Action('l', 'List everything')
@orm.db_session
def list_things_or_everything(param='all'):

    def list_project_or_everything(project_name):
        def f():
            project = orm.get(project for project in db.Project
                              if project.name == project_name)

            if project is not None:
                list_project(project)
            else:
                list_all()
        return f

    lister_dict = utils.regexdict(list_project_or_everything)
    lister_dict.update({
        'i(d(eas?)?)?': list_ideas,
        'p(rojects?)?': list_projects,
        'r(emind(ers?)?)?': list_reminders,
        's(cratch(pad)?)?': show_scratchpad,
        't(asks?)?': list_tasks,
    })

    return lister_dict[param]()


def list_all():
    list_projects()
    list_tasks()
    list_ideas()
    list_reminders()
    show_scratchpad()


def show_scratchpad():
    scratchpad_content = db.get_scratchpad_content()
    if scratchpad_content:
        print('SCRATCHPAD')
        print('----------')
        print(scratchpad_content)


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


def _generate_project_choices():
    return ui.generate_choices(db.Project.select(),
                               lambda project: project.name)


def _ask_deadline():
    return ui.pick_date('When would you like to see this finished?',
                        'All right, setting deadline at {}.')


def _ask_importance():
    return ui.ask_on_scale('On a scale from 1 to 10, how important is this?')


def _ask_duration():
    return ui.ask_timedelta('How long do you think it will take?')


def _ask_delegation():
    print('This task is urgent but not that important. You should delegate it'
          ' if possible.')
    return ui.ask('Who will you delegate this to?'
                  ' (Just hit enter for no one.)')


def _most_urgent():
    try:
        deadlined_tasks = (t for t in db.Task.select()
                           if t.deadline is not None and t.waiting_for is None)
        return orm.max(deadlined_tasks, key=lambda task: task.deadline)
    except ValueError:
        return None


def _most_important():
    try:
        important_tasks = (t for t in db.Task.select()
                           if t.importance is not None and
                           t.waiting_for is None)
        return orm.max(important_tasks, key=lambda task: task.importance)
    except ValueError:
        return None


MAIN_ACTIONS = [
    what_now,
    new_task,
    new_project,
    new_idea,
    new_reminder,
    open_scratchpad,
    list_things_or_everything,
    quit,
]
