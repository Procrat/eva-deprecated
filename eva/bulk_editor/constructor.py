from collections import namedtuple

from eva.db import Project, Scratchpad, Task

Tasks = namedtuple('Tasks', ['tasks'])
Ideas = namedtuple('Ideas', ['ideas'])
Reminders = namedtuple('Reminders', ['reminders'])


def make_project(name, tasks):
    name = name.strip()
    return Project(name=name, tasks=tasks)


def make_tasks(tasks):
    return Tasks(tasks)


def make_ideas(ideas):
    return Ideas(ideas)


def make_reminders(reminders):
    return Reminders(reminders)


def make_scratchpad(scratchpad):
    return Scratchpad(content=scratchpad)


def make_task(content, metadata, subtasks):
    metadata = metadata or {}

    id_ = metadata.get('id')
    deadline = metadata.get('deadline')
    duration = metadata.get('duration')
    importance = metadata.get('importance')
    waiting_for = metadata.get('waiting_for')

    subtasks = subtasks or []

    task = Task(content=content, deadline=deadline, duration=duration,
                importance=importance, waiting_for=waiting_for,
                subtasks=subtasks)

    if id_:
        task.id = id_

    return task


def make_metadata(id_, metadata_list):
    metadata = dict(metadata_list)
    metadata['id'] = id_
    return metadata


def make_duration(content):
    return ('duration', content)


def make_importance(content):
    return ('importance', content)


def make_waiting_for(content):
    return ('waiting_for', content)


def make_deadline(content):
    return ('deadline', content)
