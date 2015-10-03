import re

import date_utils
import parsley

GRAMMAR = """
todo_list = ws section*
section = (tasks | ideas | reminders | scratchpad | project):section ws -> section

project = normalstr:name underline indent? task*:tasks dedent? -> (name, tasks)
tasks = 'TASKS' underline indent? task*:tasks dedent? -> ('TAKEN', tasks)
ideas = 'IDEAS' underline indent? idea*:ideas dedent? -> ('IDEEN', ideas)
reminders = 'REMINDERS' underline indent? reminder*:reminders dedent? -> ('REMINDERS', reminders)
scratchpad = 'SCRATCHPAD' underline normalblock:scratchpad -> ('SCRATCHPAD', scratchpad)

task = bullet bulletlessline+:task metadata?:metadata subtasks?:subtasks -> (task, metadata, subtasks)
bulletlessline = ~bullet line
idea = bullet line
reminder = bullet line

subtasks = newline* indent task+:tasks dedent -> tasks

metadata = '[' metadatum (',' metadatum)* ']' newline
metadatum = duration | importance | waiting_for | deadline
duration = ('D' | 'd') ':' hspace normalstr
importance = ('I' | 'i') ':' hspace normalstr
waiting_for = ('W' | 'w') 'ait for' hspace normalstr
deadline = ?(parse_datetime)

bullet = '-' hspace
spacechar = ' ' | '\t'
hspace = spacechar*
newline = '\n' | '\r' '\n'?
blankline = hspace newline
ws = (spacechar | newline)*
line = ~newline normalstr:content newline -> content
underline = newline '='+ newline

indent = '@INDENT@'
dedent = '@DEDENT@'

normalblock = ~section (normalstr newline)*:content -> content
normalstr = ~indent ~dedent <normalchar+>
normalchar = ~(specialchar | newline) anything
specialchar = '[' | ']'
"""


def parse(text):
    text = tokenize_indentation(text)

    grammar = parsley.makeGrammar(GRAMMAR, {
        'parse_datetime': date_utils.parse_datetime,
    })

    return grammar(text).todo_list()


def tokenize_indentation(text):
    new_text = ''
    previous_indentation = 0
    whitespace_regex = re.compile(r'\s*')

    for line in text.splitlines():
        match = whitespace_regex.match(line)
        indentation = match.end()
        if indentation > previous_indentation:
            new_text += '@INDENT@'
        elif indentation < previous_indentation:
            new_text += '@DEDENT@'
        new_text += line[indentation:] + '\n'
        previous_indentation = indentation

    if indentation > 0:
        new_text += '@DEDENT@'

    return new_text


# TODO
def pprint():
    pass
