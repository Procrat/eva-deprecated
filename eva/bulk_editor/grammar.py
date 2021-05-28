# flake8: noqa

from collections import namedtuple

import parsley

from eva import date_utils
from eva.bulk_editor import constructor

GRAMMAR = """
todo_list = ws section*
section = (tasks | ideas | reminders | scratchpad | project):section ws -> section

project = normalstr:name underline indent?:indented task*:tasks dedent?:dedented ?(same_indent(indented, dedented)) -> make_project(name, tasks)
tasks = 'TASKS' underline indent? task*:tasks dedent? -> make_tasks(tasks)
ideas = 'IDEAS' underline indent? idea*:ideas dedent? -> make_ideas(ideas)
reminders = 'REMINDERS' underline indent? reminder*:reminders dedent? -> make_reminders(reminders)
scratchpad = 'SCRATCHPAD' underline normalblock:scratchpad -> make_scratchpad(scratchpad)

task = bullet normalstr:content metadata?:metadata newline+ subtasks?:subtasks newline* -> make_task(content, metadata, subtasks)
idea = bullet line
reminder = bullet line

subtasks = indent task+:tasks dedent -> tasks

metadata = '[' (id ',')?:id metadatum:head (',' hspace metadatum)*:tail ']' -> make_metadata(id, [head] + tail)
id = <digit+>:id -> int(id)
metadatum = duration | importance | waiting_for | deadline
duration = ('D' | 'd') ':' hspace metadatumstr:content !(parse_timedelta(content)):parsed -> make_duration(parsed)
importance = ('I' | 'i') ':' hspace metadatumstr:content -> make_importance(content)
waiting_for = ('W' | 'w') 'ait for' hspace metadatumstr:content -> make_waiting_for(content)
deadline = ('U' | 'u') ':' hspace metadatumstr:content !(parse_datetime(content)):parsed -> make_deadline(parsed)

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
    'make_project': constructor.make_project,
    'make_tasks': constructor.make_tasks,
    'make_ideas': constructor.make_ideas,
    'make_reminders': constructor.make_reminders,
    'make_scratchpad': constructor.make_scratchpad,
    'make_task': constructor.make_task,
    'make_metadata': constructor.make_metadata,
    'make_duration': constructor.make_duration,
    'make_importance': constructor.make_importance,
    'make_waiting_for': constructor.make_waiting_for,
    'make_deadline': constructor.make_deadline,
    'parse_datetime': date_utils.parse_datetime,
    'parse_timedelta': date_utils.parse_timedelta,
    'same_indent': lambda indent, dedent: bool(indent) == bool(dedent)
})
