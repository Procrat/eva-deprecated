import exceptions
import os
import subprocess
import tempfile
from collections import namedtuple
from datetime import datetime

import date_utils

YES_ANSWERS = ('y', 'yes', 'yep', 'yeah', 'sure', 'ok', 'affirmitive', 'aye',
               'k', 'kay', 'okay', 'kk')
NO_ANSWERS = ('n', 'no', 'nope', 'nop', 'nah', 'nein', 'negative')

Choice = namedtuple('Choice', ('mnemonic', 'name', 'item'))


def ask(question: str) -> str:
    """Prints question and returns user input. Waits for newline."""

    print(question)
    answer = input('> ').strip()
    return answer


def ask_polar_question(question: str) -> bool:
    """Prints question (preferably a yes-no question) and returns a boolean
    according to user input (yes = True, no = False).
    """
    while True:
        answer = ask(question).lower()
        if answer in YES_ANSWERS:
            return True
        elif answer in NO_ANSWERS:
            return False
        else:
            print("Sorry, I couldn't understand that.")


def pick_date(question: str, replay: str) -> datetime:
    """Prints question and returns a datetime or None."""

    while True:
        answer = ask(question).lower()
        if not answer:
            return None

        date = date_utils.parse(answer)
        if date:
            replay = replay.format(date_utils.format(date))
            if ask_polar_question(replay + '  Affirmative?'):
                return date
        else:
            print("Sorry, I couldn't understand that.")


def let_choose(question: str, possibilities: [Choice], none_option=None) -> str:
    """Prints possibilities and lets user select one through a mnemonic."""

    print(question)

    if none_option is not None:
        possibilities = possibilities.copy()
        possibilities.append(Choice('', none_option, None))

    for possibility in possibilities:
        print('  ({}) {}'.format(possibility.mnemonic, possibility.name))

    char = input('> ').strip().lower()
    answers = [p for p in possibilities if p.mnemonic == char]

    if len(answers) == 1:
        return answers[0].item
    elif len(answers) < 1:
        return None
    else:  # > 1
        raise exceptions.MultipleChoicesWithSameMnemonicException()


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


def generate_choices(choices, name_selector, mnemonic_selector):
    mnemonics = {}
    no_mnemonic_possible_counter = 0

    for choice in choices:
        for letter in mnemonic_selector(choice):
            if letter not in mnemonics:
                break
        else:
            letter = str(no_mnemonic_possible_counter)
            no_mnemonic_possible_counter += 1

        yield Choice(letter, name_selector(choice), choice)
