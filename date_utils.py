"""
This module handles easy date and time picking using timedelta, dateutil and
relativedelta
"""
import re
from datetime import datetime
from time import mktime

import parsedatetime


def parse(datestring: str, default=None) -> datetime:
    cal = parsedatetime.Calendar()

    time_struct, parse_status = cal.parse(datestring)

    # Parse returns 0 as parse_status if nothing is parsed
    if parse_status:
        return datetime.fromtimestamp(mktime(time_struct))
    else:
        None


def format(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")
