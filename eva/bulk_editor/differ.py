from eva import db


class ChangeDiffMixin:
    def __init__(self, object_, from_, to):
        self.object_ = object_
        self.from_ = from_
        self.to = to

    def __str__(self):
        return '{}\n  -> {}'.format(self.from_, self.to)


class DiffWithSubDiffsMixin:
    def __init__(self, parts):
        self.parts = parts

    def __str__(self):
        return '\n  '.join(line for diff in self.parts
                           for line in str(diff).split('\n'))


class ProjectAdded:
    def __init__(self, project):
        self.project = project


class ProjectRemoved:
    def __init__(self, project):
        self.project = project


class ProjectChanged(DiffWithSubDiffsMixin):
    pass


class ProjectNameChanged(ChangeDiffMixin):
    pass


class TaskAdded:
    def __init__(self, task):
        self.task = task


class TaskRemoved:
    def __init__(self, task):
        self.task = task


class TaskChanged(DiffWithSubDiffsMixin):
    pass


class ContentChanged(ChangeDiffMixin):
    pass


class DeadlineChanged(ChangeDiffMixin):
    pass


class DurationChanged(ChangeDiffMixin):
    pass


class ImportanceChanged(ChangeDiffMixin):
    pass


class WaitingForChanged(ChangeDiffMixin):
    pass


class IdeaAdded:
    def __init__(self, idea):
        self.idea = idea


class IdeaRemoved:
    def __init__(self, idea):
        self.idea = idea


class ReminderAdded:
    def __init__(self, reminder):
        self.reminder = reminder


class ReminderRemoved:
    def __init__(self, reminder):
        self.reminder = reminder


class ReminderTimeChanged(ChangeDiffMixin):
    pass


def diff(sections):
    """Makes a diff with the state of the database."""

    # TODO handle section removal
    return [diff_section(section) for section in sections]


def diff_section(section):
    # TODO handle ideas, reminders
    assert isinstance(db.Project, section)  # TODO
    db_project = db.Project.select(name=section.name)
    parts = diff_project_parts(db_project, section)
    return ProjectChanged(parts)


def diff_project_parts(db_project, project):
    return [diff_task(task, project) for task in project.tasks]


def diff_task(task, parent):
    try:
        id_ = task.id
    except AttributeError:
        return TaskAdded(task)

    db_task = db.Task.get(id_)
    print('Task with id=%d found in DB:' % id_, db_task)

    parts = list(diff_task_parts(db_task, task))
    return TaskChanged(parts)


def diff_task_parts(db_task, task):
    if task.deadline != db_task.deadline:
        yield DeadlineChanged(db_task.deadline, task.deadline)
    if task.duration != db_task.duration:
        yield DurationChanged(db_task.duration, task.duration)
    if task.importance != db_task.importance:
        yield ImportanceChanged(db_task.importance, task.importance)
    if task.waiting_for != db_task.waiting_for:
        yield WaitingForChanged(db_task.waiting_for, task.waiting_for)

    if task.content != db_task.content:
        yield ContentChanged(db_task.content, task.content)

    for subtask in task.subtasks:
        yield diff_task(subtask, task)
