"""
The runner of lectioexporter.
"""
from lectio import Session
from lectio.utilities import lookup_values
from lectio.types import AssignmentStatuses

from operator import attrgetter

from .google_calendar import clear_calendar, create_event
from .google_calendar import make_service

from .evernote import get_evernote_token, make_note

from evernote.api.client import EvernoteClient

from .credentials import get_google_credentials, get_lectio_credentials

from .database import Database

from .config import CALENDAR_ID, SCHOOL_ID, STUDENT_ID, WEEKS_TO_CHECK
from .config import LOOKUP_TEACHERS, LOOKUP_GROUPS
from .config import GOOGLE_ENABLED, EVERNOTE_ENABLED
from .config import TIMEZONE
from .config import EVERNOTE_NOTEBOOK_GUID
from .config import EVERNOTE_ASSIGNMENT_PREFIX, EVERNOTE_HOMEWORK_PREFIX

from .utilities import get_current_year, get_current_week

import logging

logger = logging.getLogger("LectioExporter")


def period_to_calendar(service, calendar_id, period):
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

    desc_items.append("Id: " + period.id)

    description = "\n \n".join(desc_items)

    # Start time and end time
    starttime = period.starttime
    endtime = period.endtime

    result = create_event(service, calendar_id, summary, status, location,
                          description, starttime, endtime)

    return result


def main_google(session, database):
    """
    Synchronizes the Lectio timetable with Google Calendar.
    """
    credentials = get_google_credentials()

    service = make_service(credentials)

    year = get_current_year()
    week = get_current_week()

    periods = []
    for i in range(WEEKS_TO_CHECK):
        logger.info("Getting time table for week {}, {}".format(str(week + i),
                                                                str(year)))
        periods.extend(session.get_periods(week + i, year,
                                           student_id=STUDENT_ID))

    periods.sort(key=attrgetter("starttime"))
    min_time = periods[0].starttime

    ids_to_keep = []
    periods_to_commit = []

    for period in periods:
        if database.get(period.id) != period.get_hash():
            periods_to_commit.append(period)
        else:
            ids_to_keep.append(period.id)

    clear_calendar(service, CALENDAR_ID, except_ids=ids_to_keep,
                   min_time=min_time)

    for period in periods_to_commit:
        database[period.id] = period.get_hash()
        period_to_calendar(service, CALENDAR_ID, period)


def main_evernote(session):
    """
    Synchronizes Lectio homework and assignments with Evernote.
    """
    token = get_evernote_token()

    logger.info("Creating Evernote client.")
    client = EvernoteClient(token=token, sandbox=False)
    user_store = client.get_user_store()
    note_store = client.get_note_store()

    logger.info("Getting Lectio assignments.")
    assignments = session.get_assignments()

    for assignment in assignments:
        title = EVERNOTE_ASSIGNMENT_PREFIX + assignment.title

        content = ""

        if assignment.note:
            content += assignment.note
            content += "\n\n" + "-" * 30 + "\n\n"

        content += "Hold: {}.\n".format(assignment.group)
        content += "Elevtid: {} timer.\n".format(assignment.student_hours)
        content += "Afleveringsfrist: {}.".format(assignment.deadline)

        content = content.replace("\n", "<br/>")

        note = make_note(token, note_store, title, content)


def main():
    """
    Exports Lectio to Google Calendar and Todoist.
    """
    session = Session(SCHOOL_ID, tz=TIMEZONE)

    lectio_credentials = get_lectio_credentials()

    session.auth(lectio_credentials["username"],
                 lectio_credentials["password"])

    if GOOGLE_ENABLED:
        database = Database()
        database.load()

        main_google(session, database)

        database.save()

    if EVERNOTE_ENABLED:
        main_evernote(session)


if __name__ == '__main__':
    main()
