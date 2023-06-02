"""SQLite adapters and converters for unsupported data types."""

from datetime import date, timedelta
from decimal import Decimal

from packaging import version
from pytimeparse.timeparse import timeparse
from unidecode import unidecode


def adapt_decimal(value):
    """Convert decimal.Decimal to string."""
    return str(value)


def convert_decimal(value):
    """Convert string to decimalDecimal."""
    return Decimal(str(value.decode()))


def adapt_timedelta(value):
    """Convert datetime.timedelta to %H:%M:%S string."""
    hours, remainder = divmod(value.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def convert_timedelta(value):
    """Convert %H:%M:%S string to datetime.timedelta."""
    return timedelta(seconds=timeparse(value.decode()))


def unicase_compare(string_1, string_2):
    """Taken from https://github.com/patarapolw/ankisync2/issues/3#issuecomment-768687431."""
    _string_1 = unidecode(string_1).lower()
    _string_2 = unidecode(string_2).lower()
    return 1 if _string_1 > _string_2 else -1 if _string_1 < _string_2 else 0


def convert_date(value):
    """Handle SQLite date conversion."""
    try:
        return date.fromisoformat(value.decode())
    except ValueError as err:
        raise ValueError("DATE field contains {}".format(err))  # pylint: disable=W0707


def check_sqlite_table_xinfo_support(version_string):
    """Check for SQLite table_xinfo support."""
    sqlite_version = version.parse(version_string)
    if sqlite_version.major > 3 or (sqlite_version.major == 3 and sqlite_version.minor >= 26):
        return True
    return False
