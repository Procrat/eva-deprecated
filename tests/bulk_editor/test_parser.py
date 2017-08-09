from pathlib import Path

import pytest

from eva import bulk_editor

TODO_FILES = (Path(__file__) / '..' / 'todo_files').resolve().glob('*')


@pytest.mark.parametrize('todo_filename', TODO_FILES)
def test_editor(todo_filename):
    with open(str(todo_filename)) as todo_file:
        bulk_editor.parse(todo_file.read())
        return True
