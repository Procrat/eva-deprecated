from pony.orm import Database, Required, Set, Optional

db = Database()


class Task(db.Entity):
    content = Required(str, unique=True)
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')

    def __str__(self):
        s = '- {}'.format(self.content)
        s += ''.join('\n  - {}'.format(task) for task in self.subtasks)
        return s


class Idea(db.Entity):
    content = Required(str, unique=True)

    def __str__(self):
        return '- {}'.format(self.content)
