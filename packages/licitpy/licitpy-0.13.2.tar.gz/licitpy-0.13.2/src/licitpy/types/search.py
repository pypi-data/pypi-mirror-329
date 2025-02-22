from enum import Enum


class TimeRange(Enum):
    TODAY = "today"
    FROM_YESTERDAY = "from_yesterday"
    THIS_MONTH = "this_month"
    LAST_THREE_MONTHS = "last_three_months"
    LAST_SIX_MONTHS = "last_six_months"
    LAST_YEAR = "last_year"
