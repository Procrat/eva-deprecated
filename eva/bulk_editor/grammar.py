# flake8: noqa

from collections import namedtuple

import parsley

from eva import date_utils

GRAMMAR = """
todo_list = ws section*
section = (tasks | ideas | reminders | scratchpad | project):section ws -> section

project = normalstr:name underline indent?:indented task*:tasks dedent?:dedented ?(same_indent(indented, dedented)) -> (name, tasks)
tasks = 'TASKS' underline indent? task*:tasks dedent? -> ('TASKS', tasks)
ideas = 'IDEAS' underline indent? idea*:ideas dedent? -> ('IDEAS', ideas)
reminders = 'REMINDERS' underline indent? reminder*:reminders dedent? -> ('REMINDERS', reminders)
scratchpad = 'SCRATCHPAD' underline normalblock:scratchpad -> ('SCRATCHPAD', scratchpad)

task = bullet normalstr:content metadata?:metadata newline+ subtasks?:subtasks newline* -> Task(content, metadata, subtasks)
idea = bullet line
reminder = bullet line

subtasks = indent task+:tasks dedent -> tasks

metadata = '[' metadatum:head (',' hspace metadatum)*:tail ']' -> [head] + tail
metadatum = duration | importance | waiting_for | deadline
duration = ('D' | 'd') ':' hspace metadatumstr:content -> ('duration', content)
importance = ('I' | 'i') ':' hspace metadatumstr:content -> ('importance', content)
waiting_for = ('W' | 'w') 'ait for' hspace metadatumstr:content -> ('waiting for', content)
deadline = metadatumstr:content !(parse_datetime(content)):parsed -> ('deadline', parsed)

bullet = ('-' | '*' | '+') hspace
spacechar = ' ' | '\t'
hspace = spacechar*
newline = '\n' | '\r' '\n'?
blankline = hspace newline
ws = (spacechar | newline)*
line = normalstr:content newline+ -> content
underline = newline '='+ newline
metadatumstr = <metadatumchar+>

indent = '@INDENT@'
dedent = '@DEDENT@'

normalblock = ~section (normalstr newline)*:content -> content
normalstr = ~indent ~dedent <normalchar+>
normalchar = ~(specialchar | newline) anything
metadatumchar = ~(',' | ':') normalchar
specialchar = '[' | ']'
"""

Task = namedtuple('Task', ['content', 'metadata', 'subtasks'])

grammar = parsley.makeGrammar(GRAMMAR, {
    'parse_datetime': date_utils.parse_datetime,
    'Task': Task,
    'same_indent': lambda indent, dedent: bool(indent) == bool(dedent)
})
