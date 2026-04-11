from datetime import datetime

from dateparser import parse

from moleql.mql.errors import FilterError

_DATE_PARSE_ERROR: str = "Invalid date value: {date!r}"


def _invoke_date_parser(date: str) -> datetime | None:
    """Computation: delegates string parsing to the dateparser library."""
    return parse(date, languages=["en"])


def _require_date_result(result: datetime | None, original: str) -> datetime:
    """Computation: returns the datetime result, or raises FilterError if None."""
    if result is None:
        raise FilterError(_DATE_PARSE_ERROR.format(date=original))
    return result


def parse_date(date: str) -> datetime:
    """Coordinator: parses a date string and raises FilterError on invalid input."""
    result = _invoke_date_parser(date)
    return _require_date_result(result, date)
