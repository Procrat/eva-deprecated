from pony.orm import Database, Required, Set, Optional, PrimaryKey

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

    def __str__(self):
        s = '- {}'.format(self.content)
        s += '\n  '.join(str(task.content.split('\n'))
                         for task in self.subtasks)
        return s


class Idea(db.TodoItem):
    pass


class Scratchpad(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Optional(str)


def get_scratchpad():
    query_result = Scratchpad.select().for_update()[:1]
    return query_result[0] if query_result else Scratchpad(content='')
