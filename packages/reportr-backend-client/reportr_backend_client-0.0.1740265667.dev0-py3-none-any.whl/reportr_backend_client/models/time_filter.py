from enum import Enum


class TimeFilter(str, Enum):
    LATEST = "latest"
    THIS_MONTH = "this_month"
    THIS_WEEK = "this_week"
    TODAY = "today"

    def __str__(self) -> str:
        return str(self.value)
