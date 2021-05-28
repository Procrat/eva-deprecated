#  import collections
#  import copy
#  import datetime

#  from pony import orm
#  import pytest

#  from eva import db
#  from eva import settings
#  from eva.bulk_editor import differ

#  DiffCase = collections.namedtuple('DiffCase', ['changed_sections',
#                                                 'expected_diffs'])


#  @pytest.fixture(scope="module")
#  def setup_db():
#      settings.setup(settings.TESTING)


#  @pytest.fixture
#  def changed_task():
#      return 'Hoi 1'


#  @pytest.fixture
#  def changed_project():
#      return 'Hoi 2'


#  @pytest.fixture
#  def case1():
#      with orm.db_session():
#      task = db.Task(content='do stuff',
#                     duration=datetime.timedelta(hours=1))
#      edited_task = copy.copy(task)
#      edited_task.duration *= 2
#      edited_section = db.Section(name='tasks')
#      edited_section.tasks.append(edited_task)
#      expected_diff = differ.DurationChanged(task, task.duration,
#                                             edited_task.duration)
#      return DiffCase([edited_section], [expected_diff])
#      t = db.Task(content='hoi')
#      return DiffCase([], [])


#  @pytest.fixture
#  def case2():
#      return DiffCase([], [])


#  @pytest.fixture(params=['case1', 'case2'])
#  def diff_case(request):
#      return request.getfuncargvalue(request.param)


#  def test_all_in(setup_db, diff_case):
#      diffs = differ.diff(diff_case.changed_sections)
#      assert diffs == diff_case.expected_diffs


def test_x():
    from eva import settings
    from eva.bulk_editor import parse, printer
    from pathlib import Path

    settings.setup(settings.TESTING)

    path = (Path(__file__) / '..' / '..' / '..' / 'tests' / 'bulk_editor' /
            'todo_files' / 'todo_file').resolve()
    with open(str(path)) as file_:
        text = file_.read()
    sasdf = parse(text)
    print(printer.stringify(sasdf))
