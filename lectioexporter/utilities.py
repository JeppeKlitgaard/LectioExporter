"""
Contains utility functions and classes used by LectioExporter.
"""

from datetime import datetime


def dt2rfc3339(dt):
    """
    Converts a ``datetime`` object to a RFC3339-formatted ``str``.
    """
    return dt.isoformat()


def rfc33392dt(string):
    """
    Converts a RFC3339-formatted ``str`` to a ``datetime`` object.
    """
    string = string.replace(":", "")  # Hacky fix for %z
    fmt = r"%Y-%m-%dT%H%M%S%z"

    return datetime.strptime(string, fmt)


def _get_cal():
    """
    Returns a tuple containing:
        (year, week_number, day_of_week).
    """
    now = datetime.today()

    return now.isocalendar()


def get_current_week():
    """
    Returns the current week number.
    """
    return _get_cal()[1]


def get_current_year():
    """
    Returns the current year.
    """
    return _get_cal()[0]
