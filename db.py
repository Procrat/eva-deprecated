from datetime import datetime

import date_utils
from pony.orm import Database, Optional, PrimaryKey, Required, Set

db = Database()


class Project(db.Entity):
    name = PrimaryKey(str)
    tasks = Set('Task', reverse='project')
    deadline = Optional(datetime)


class TodoItem(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(str)

    def __str__(self):
        return '- {}'.format(self.content)


class Task(db.TodoItem):
    project = Optional('Project', reverse='tasks')
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')
    deadline = Optional(datetime)

    def __str__(self):
        s = '- {}'.format(self.content)
        s += '\n  '.join(str(task.content.split('\n'))
                         for task in self.subtasks)
        return s


class Idea(db.TodoItem):
    pass


class Reminder(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(str)
    when = Required(datetime)

    def __str__(self):
        return '- {} @ {}'.format(self.content, date_utils.format(self.when))


class Scratchpad(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Optional(str)


def get_scratchpad() -> Scratchpad:
    query_result = Scratchpad.select().for_update()[:1]
    return query_result[0] if query_result else Scratchpad(content='')
