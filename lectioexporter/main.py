"""
The runner of lectioexporter.
"""
from lectio import Session
from lectio.utilities import lookup_values

from operator import attrgetter

from .google_calendar import clear_calendar, create_event
from .google_calendar import get_credentials, make_service
from .config import CALENDAR_ID, SCHOOL_ID, STUDENT_ID, WEEKS_TO_CHECK
from .config import LOOKUP_TEACHERS, LOOKUP_GROUPS
from .utilities import get_current_year, get_current_week


def period_to_calendar(service, calendarId, period):
    """
    Takes ``Period`` object and adds an event on a calendar for it.
    """
    MUST_NOT_BE_NONE = ("starttime", "endtime", "groups")

    for value in MUST_NOT_BE_NONE:
        if getattr(period, value) is None:
            error = "Period.'{}'' must not be None!".format(value)
            raise AttributeError(error)

    # Summary
    groups = lookup_values(period.groups, LOOKUP_GROUPS)
    summary = ", ".join(groups)

    if period.teachers_short is not None:
        teachers = lookup_values(period.teachers_short, LOOKUP_TEACHERS)
        summary += " - {}".format(", ".join(teachers))

    if period.rooms is not None:
        summary += " - {}".format(", ".join(period.rooms))

    # Status
    status = "confirmed"

    # Location
    if period.rooms:
        location = ", ".join(period.rooms)
    else:
        location = ""

    # Description
    desc_items = []
    if period.topic:
        desc_items.append(period.topic)

    if period.homework:
        desc_items.append("Lektier:\n" + period.homework)

    if period.note:
        desc_items.append("Note:\n" + period.note)

    description = "\n \n".join(desc_items)

    # Start time and end time
    starttime = period.starttime
    endtime = period.endtime

    result = create_event(service, calendarId, summary, status, location,
                          description, starttime, endtime)

    return result


if __name__ == '__main__':
    session = Session(SCHOOL_ID)

    year = get_current_year()
    week = get_current_week()

    periods = []
    for i in range(WEEKS_TO_CHECK):
        periods.extend(session.get_periods(week + i, year,
                                           student_id=STUDENT_ID))

    credentials = get_credentials()
    service = make_service(credentials)

    # Clear all elements, except those that are before the time of the earliest
    # period.
    periods.sort(key=attrgetter("starttime"))
    clear_calendar(service, CALENDAR_ID, min_time=periods[0].starttime)

    for period in periods:
        period_to_calendar(service, CALENDAR_ID, period)
