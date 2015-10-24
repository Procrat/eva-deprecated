import exceptions
import os
import subprocess
import tempfile
from collections import namedtuple
from datetime import datetime, timedelta

import date_utils

YES_ANSWERS = ('y', 'yes', 'yep', 'yeah', 'sure', 'ok', 'affirmitive', 'aye',
               'k', 'kay', 'okay', 'kk', 'uhu')
NO_ANSWERS = ('n', 'no', 'nope', 'nop', 'nah', 'nein', 'negative',
              'not really')

Choice = namedtuple('Choice', ('mnemonic', 'name', 'item'))


def ask(question: str) -> str:
    """Prints question and returns user input. Waits for newline."""

    print(question)
    answer = input('> ').strip()
    return answer


def show(announcement: str) -> None:
    """Prints announcement."""

    print(announcement)


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


def ask_on_scale(question: str, range_=range(1, 11)) -> int:
    """Prints question (preferably asking for a number on a scale) and keeps
    asking until the user inputs a number or nothing.
    """
    while True:
        answer = ask(question)
        if answer == '':
            return None

        try:
            parsed_answer = int(answer)
            if parsed_answer in range_:
                return parsed_answer

            print('Sorry, that number is not on the scale.')
        except ValueError:
            print("Sorry, I couldn't understand that.")


def pick_date(question: str, replay_template: str) -> datetime:
    """Prints question and returns a datetime or None."""

    while True:
        answer = ask(question).lower()
        if not answer:
            return None

        date = date_utils.parse_datetime(answer)
        if date:
            replay = replay_template.format(date_utils.format(date))
            if ask_polar_question(replay + '  Affirmative?'):
                return date
        else:
            print("Sorry, I couldn't understand that.")


def ask_timedelta(question: str) -> timedelta:
    """Prints question and returns a timedelta or None."""

    while True:
        answer = ask(question).lower()
        if not answer:
            return None

        delta = date_utils.parse_timedelta(answer)
        if delta:
            return delta
        else:
            print("Sorry, I couldn't understand that.")


def let_choose(question: str,
               possibilities: [Choice],
               none_option=None,
               with_params=False):
    """
    Prints possibilities and lets user select one through a mnemonic.

    Args:
        question: A question shown to the user
        possiblities: A sequence of possible Choice items the user can choose
            from.
        none_option: A string representing what happens when the user doesn't
            input anything (and None is returned by this function)
        with_params: A boolean determining whether to also return user supplied
            parameters

    Returns:
        The possibility (Choice.item), as selected by the user
        or possibly a tuple (choice, parameters entered by the user)

    Raises:
        MultipleChoicesWithSameMnemonicException: Two possibilities with the
            same mnemonic are given.
    """
    print(question)

    if none_option is not None:
        possibilities = possibilities.copy()
        possibilities.append(Choice('', none_option, None))

    for possibility in possibilities:
        print('  ({}) {}'.format(possibility.mnemonic, possibility.name))

    command = input('> ').strip().lower()
    parts = command.split(maxsplit=1)
    if parts:
        char, *params = parts
    else:
        char, params = '', []

    answers = [p for p in possibilities if p.mnemonic == char]
    if len(answers) > 1:
        raise exceptions.MultipleChoicesWithSameMnemonicException()

    choice = answers[0].item if answers else None
    return choice, params if with_params else choice


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


def generate_choices(items, name_selector):
    """
    Generates choices with fitting mnemonics for a list of items.

    Args:
        items (List[X]): items to choose from
        name_selector (Callable[[X], str]):
            function that derives a name from an item
    Yields:
        Choice-objects for each item
    """
    mnemonics = {}
    no_mnemonic_possible_counter = 0

    for item in items:
        name = name_selector(item)
        for letter in name.lower():
            if letter not in mnemonics:
                break
        else:
            letter = str(no_mnemonic_possible_counter)
            no_mnemonic_possible_counter += 1

        yield Choice(letter, name, item)
