import math
from datetime import datetime, timedelta

from pony import orm
from pony.orm import Database, Optional, Required, Set

import date_utils

db = Database()


class Base(db.Entity):
    pass


class MetadataMixin(db.Base):
    deadline = Optional(datetime)
    duration = Optional(timedelta)
    importance = Optional(int)
    waiting_for = Optional(str)

    def has_metadata(self):
        return (self.deadline is not None or
                self.duration is not None or
                self.importance is not None or
                self.waiting_for is not None)

    def metadata(self):
        if self.waiting_for is not None:
            yield 'Waiting for {}'.format(self.waiting_for)
        if self.deadline is not None:
            yield date_utils.format(self.deadline)
        if self.duration is not None:
            yield 'D: ' + date_utils.format(self.duration)
        if self.importance is not None:
            yield 'I: ' + str(self.importance)

    def metadata_str(self):
        return ', '.join(self.metadata())

    def urgency(self):
        """Does a guess of the urgency on a scale of 1 to 10."""

        # TODO: should be a bit more intelligent than this
        # Current heuristic:
        #     10 + log2(hours needed / hours left before deadline)

        time_left = self.deadline - datetime.now()
        hours_left = timedelta(hours=5 * time_left.days,
                               seconds=time_left.seconds)
        raw_urgency = 10 + math.log2(self.duration / hours_left)
        return max(10, min(1, raw_urgency))

    def is_urgent(self):
        return self.urgency() >= 5

    def is_important(self):
        return self.importance >= 5


class Project(db.MetadataMixin):
    name = Required(str, index=True)
    tasks = Set('Task', reverse='project')

    def __str__(self):
        s = self.name.upper() + '\n'
        if self.has_metadata():
            s += ' [{}]'.format(self.metadata_str())
        s += '-' * len(self.name) + '\n'

        s += '\n'.join(str(task) for task in self.tasks)
        s += '\n'

        return s


class TodoItem(db.Base):
    content = Required(str)

    def __str__(self):
        return '- {}'.format(self.content)


class Task(db.TodoItem, db.MetadataMixin):
    project = Optional('Project', reverse='tasks')
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')

    def __str__(self):
        s = '- ' + self.content
        if self.has_metadata():
            s += ' [{}]'.format(self.metadata_str())
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
