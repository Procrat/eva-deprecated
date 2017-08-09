"""
This module handles easy date and time picking using timedelta, dateutil and
relativedelta.
"""
from datetime import datetime, timedelta
from functools import singledispatch
import re
from time import mktime

import parsedatetime


def parse_datetime(datestring: str, default=None) -> datetime:
    calendar = parsedatetime.Calendar()

    time_struct, parse_status = calendar.parse(datestring)

    # Parse returns 0 as parse_status if nothing is parsed
    if parse_status == 0:
        return None

    return datetime.fromtimestamp(mktime(time_struct))


def parse_timedelta(timedelta_str: str) -> timedelta:
    regex = r'(about\s*)?((\d+)\s*h(ours?)?)?\s*((\d+)\s*m(inutes?)?)?'
    match = re.fullmatch(regex, timedelta_str.strip().lower())

    if match is None:
        return None

    hours_str = match.group(3)
    if hours_str is None:
        return None
    hours = int(hours_str)

    minutes_str = match.group(6)
    minutes = int(minutes_str) if minutes_str is not None else 0

    return timedelta(hours=hours, minutes=minutes)


@singledispatch
def format(arg) -> str:
    raise ValueError


@format.register(datetime)
def _(dt: datetime) -> str:
    def format_time():
        if dt.minute == 0:
            return '{}h'.format(dt.hour)
        else:
            return dt.strftime('%H:%M')

    def format_date():
        return dt.strftime('%d-%m')

    if dt.date() == datetime.now().date():
        return format_time()
    elif dt.date() == (datetime.now() + timedelta(days=1)).date():
        return format_time() + ' tomorrow'
    elif dt.date() <= (datetime.now() + timedelta(days=3)).date():
        return format_date() + ' ' + format_time()
    else:
        return format_date()


@format.register(timedelta)
def _(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds // 60) - (60 * hours)
    return '{}h'.format(hours) + ('{}m'.format(minutes) if minutes > 0 else '')
