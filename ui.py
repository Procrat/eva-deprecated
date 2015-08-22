import exceptions
import os
import subprocess
import tempfile

from actions import Action


def ask(question: str) -> str:
    """Prints question and returns user input. Waits for newline."""

    print(question)
    answer = input('> ')
    return answer


def let_choose(question: str, possibilities: [Action]) -> str:
    """Prints possibilities and lets user select one through a mnemonic."""

    print(question)
    for possibility in possibilities:
        print('  ({}) {}'.format(possibility.mnemonic, possibility.name))
    char = input('> ')
    answers = [p for p in possibilities if p.mnemonic == char]

    if len(answers) == 1:
        return answers[0]
    elif len(answers) < 1:
        return None
    else:  # > 1
        raise exceptions.MultipleActionsWithSameMnemonicException()


def ask_from_editor(initial_content: str) -> str:
    """
    Open favourite editor with temporary file and return its content
    afterwards.

    Args:
        initial_content (str): initial content of the temporary file
    """
    editor = os.getenv('EDITOR') or 'xdg-open'

    temp_fd, temp_path = tempfile.mkstemp()
    try:
        with open(temp_fd, 'w') as temp_file:
            temp_file.write(initial_content)

        subprocess.check_call([editor, temp_path])

        with open(temp_path) as temp_file:
            return temp_file.read()

    except subprocess.CalledProcessError as error:
        print('Your editor (%s) exited with error code %d (%s).' %
              (editor, error.returncode, error.message))
    finally:
        os.remove(temp_path)
