from datetime import datetime

import date_utils
from pony.orm import Database, Optional, PrimaryKey, Required, Set

db = Database()


class Base(db.Entity):
    pass


class MetadataMixin(db.Base):
    deadline = Optional(datetime)
    importance = Optional(int)

    def metadata_str(self):
        metadata = []
        if self.deadline is not None:
            metadata.append(date_utils.format(self.deadline))
        if self.importance is not None:
            metadata.append(str(self.importance))
        return ', '.join(metadata)


class Project(db.MetadataMixin):
    name = Required(str, index=True)
    tasks = Set('Task', reverse='project')


class TodoItem(db.Base):
    content = Required(str)

    def __str__(self):
        return '- {}'.format(self.content)


class Task(db.TodoItem, db.MetadataMixin):
    project = Optional('Project', reverse='tasks')
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')

    def __str__(self):
        s = '- {}'.format(self.content)
        s += '\n  '.join(str(task.content.split('\n'))
                         for task in self.subtasks)
        return s


class Idea(db.TodoItem):
    pass


class Reminder(db.Entity):
    content = Required(str)
    when = Required(datetime)

    def __str__(self):
        return '- {} @ {}'.format(self.content, date_utils.format(self.when))


class Scratchpad(db.Entity):
    content = Optional(str)


def get_scratchpad() -> Scratchpad:
    query_result = Scratchpad.select().for_update()[:1]
    return query_result[0] if query_result else Scratchpad(content='')
