"""
This module handles easy date and time picking using timedelta, dateutil and
relativedelta.
"""
from datetime import datetime, timedelta
from time import mktime

import parsedatetime


def parse(datestring: str, default=None) -> datetime:
    calendar = parsedatetime.Calendar()

    time_struct, parse_status = calendar.parse(datestring)

    # Parse returns 0 as parse_status if nothing is parsed
    if parse_status == 0:
        return None

    return datetime.fromtimestamp(mktime(time_struct))


def format(dt: datetime) -> str:
    if dt.date() == datetime.now().date():
        return dt.strftime('%H:%M')
    elif dt.date() == (datetime.now() + timedelta(days=1)).date():
        return dt.strftime('%H:%M tomorrow')
    elif dt.date() <= (datetime.now() + timedelta(days=3)).date():
        return dt.strftime('%d-%m-%Y %H:%M')
    else:
        return dt.strftime('%d-%m-%Y')
