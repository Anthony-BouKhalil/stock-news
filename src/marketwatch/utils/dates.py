from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

TORONTO_TIMEZONE = ZoneInfo("America/Toronto")


def current_toronto_time() -> datetime:
    return datetime.now(TORONTO_TIMEZONE)


def report_date() -> str:
    return current_toronto_time().strftime("%B %d, %Y")


def report_timestamp() -> str:
    return current_toronto_time().strftime("%B %d, %Y at %I:%M %p")
