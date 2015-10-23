from datetime import datetime

from pony import orm
from pony.orm import Database, Optional, PrimaryKey, Required, Set

import date_utils

db = Database()


class Project(db.Entity):
    name = PrimaryKey(str)
    tasks = Set('Task', reverse='project')


class TodoItem(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(str)

    def __str__(self):
        return '- {}'.format(self.content)


class Task(db.TodoItem):
    project = Optional('Project', reverse='tasks')
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')
    finished = Required(bool, default=False)

    def __str__(self):
        s = '- {}'.format(self.content)
        s += '\n  '.join(str(task.content.split('\n'))
                         for task in self.subtasks)
        return s

    def _finish(self):
        self.finished = True

    def finish(self):
        _finish(self) if self.project else self.delete()


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



@orm.db_session
def get_scratchpad() -> Scratchpad:
    query_result = Scratchpad.select()[:1]
    return query_result[0] if query_result else Scratchpad(content='')


@orm.db_session
def get_scratchpad_content() -> str:
    return get_scratchpad().content


@orm.db_session
def set_scratchpad_content(new_content):
    get_scratchpad().content = new_content
