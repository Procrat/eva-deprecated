from pony.orm import Database, Required, Set, Optional

db = Database()


class Task(db.Entity):
    content = Required(str, unique=True)
    subtasks = Set('Task', reverse='parent_task')
    parent_task = Optional('Task', reverse='subtasks')


class Idea(db.Entity):
    content = Required(str, unique=True)
