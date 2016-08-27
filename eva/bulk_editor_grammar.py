# flake8: noqa

from collections import namedtuple

import parsley

from eva import date_utils

GRAMMAR = """
todo_list = ws section*
section = (tasks | ideas | reminders | scratchpad | project):section ws -> section

project = normalstr:name underline indent?:indented task*:tasks dedent?:deindented ?(indented == deindented) -> (name, tasks)
tasks = 'TASKS' underline indent? task*:tasks dedent? -> ('TASKS', tasks)
ideas = 'IDEAS' underline indent? idea*:ideas dedent? -> ('IDEAS', ideas)
reminders = 'REMINDERS' underline indent? reminder*:reminders dedent? -> ('REMINDERS', reminders)
scratchpad = 'SCRATCHPAD' underline normalblock:scratchpad -> ('SCRATCHPAD', scratchpad)

task = bullet bulletlessline:task metadata?:metadata subtasks?:subtasks newline* -> Task(task, metadata, subtasks)
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

bullet = ('-' | '*' | '+') hspace
spacechar = ' ' | '\t'
hspace = spacechar*
newline = '\n' | '\r' '\n'?
blankline = hspace newline
ws = (spacechar | newline)*
line = normalstr:content newline+ -> content
underline = newline '='+ newline

indent = '@INDENT@'
dedent = '@DEDENT@'

normalblock = ~section (normalstr newline)*:content -> content
normalstr = ~indent ~dedent <normalchar+>
normalchar = ~(specialchar | newline) anything
specialchar = '[' | ']'
"""

Task = namedtuple('Task', ['content', 'metadata', 'subtasks'])

grammar = parsley.makeGrammar(GRAMMAR, {
    'parse_datetime': date_utils.parse_datetime,
    'Task': Task,
})
