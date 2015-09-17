"""
This module handles easy date and time picking using timedelta, dateutil and
relativedelta.
"""
from datetime import datetime
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
    return dt.strftime("%Y-%m-%d %H:%M")
