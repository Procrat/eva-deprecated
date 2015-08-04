from actions import Action
import exceptions


def ask(question: str) -> str:
    """Prints question and returns user input. Waits for newline."""

    print(question)
    answer = input('> ')
    return answer


def let_choose(question, possibilities: [Action]) -> str:
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
