import re

from eva.bulk_editor.grammar import grammar

WHITESPACE_REGEX = re.compile(r'\s*')
WHITESPACE_WITH_DASH_REGEX = re.compile(r'\s*(-\s+)?')
INDENT = '@INDENT@'
DEDENT = '@DEDENT@'


def parse(text):
    text = combine_continuations(text)
    print(text)
    text = tokenize_indentation(text)
    print(text)

    return grammar(text).todo_list()


def combine_continuations(text):
    new_text = ''
    previous_indentation = 0
    previous_was_list_item = False

    for line in text.splitlines():
        indent_match = WHITESPACE_REGEX.match(line)
        indentation = indent_match.end()
        content = line[indentation:]
        current_is_list_item = content.startswith('- ')

        is_list_item_continuation = (previous_was_list_item and
                                     not current_is_list_item and
                                     indentation == previous_indentation)
        if is_list_item_continuation:
            new_text = new_text[:-1] + ' ' + content + '\n'
        else:
            new_text += line + '\n'

        previous_indentation = WHITESPACE_WITH_DASH_REGEX.match(line).end()
        previous_was_list_item = (content.startswith('- ') or
                                  is_list_item_continuation)

    return new_text


def tokenize_indentation(text):
    new_text = ''
    previous_indentations = []

    for line_no, line in enumerate(text.splitlines()):
        match = WHITESPACE_REGEX.match(line)
        indentation = match.end()
        previous_indentation = sum(previous_indentations)
        indentation_diff = indentation - previous_indentation
        if indentation > previous_indentation:
            new_text += INDENT
            previous_indentations.append(indentation_diff)
        elif indentation < previous_indentation:
            for i in range(len(previous_indentations) - 1, -1, -1):
                last_indent = sum(previous_indentations[i:])
                if last_indent == -indentation_diff:
                    new_text += (len(previous_indentations) - i) * DEDENT
                    previous_indentations = previous_indentations[:i]
                    break
            else:
                context = '\n'.join(text.splitlines()[line_no - 2:line_no + 3])
                raise Exception(
                    'Wrong indentation level at:\n{}\n'
                    'Previous indents: {}\nIndent now: {}\nDiff: {}'
                    .format(context, previous_indentations, indentation,
                            indentation_diff))
        new_text += line[indentation:] + '\n'

    if len(previous_indentations) > 0:
        new_text += len(previous_indentations) * DEDENT

    return new_text


# TODO
def pprint():
    pass
