"""
The runner of lectioexporter.
"""
from lectio import Session
from lectio.utilities import lookup_values
from lectio.types import AssignmentStatuses

from operator import attrgetter

import todoist

from .google_calendar import clear_calendar, create_event
from .google_calendar import make_service

from .credentials import (get_google_credentials, get_todoist_credentials,
                          get_lectio_credentials)

from .database import Database

from .config import CALENDAR_ID, SCHOOL_ID, STUDENT_ID, WEEKS_TO_CHECK
from .config import LOOKUP_TEACHERS, LOOKUP_GROUPS
from .config import GOOGLE_ENABLED, TODOIST_ENABLED
from .config import PROJECT_ID, TIMEZONE

from .utilities import get_current_year, get_current_week

import logging

logger = logging.getLogger("LectioExporter")


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

    desc_items.append("Id: " + period.id)

    description = "\n \n".join(desc_items)

    # Start time and end time
    starttime = period.starttime
    endtime = period.endtime

    result = create_event(service, calendarId, summary, status, location,
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


def main_todoist(session):
    """
    Synchronizes the Lectio assignments with Todoist.
    """
    todoist_credentials = get_todoist_credentials()
    lectio_credentials = get_lectio_credentials()

    logger.info("Creating Todoist service.")
    service = todoist.TodoistAPI()
    service.login(todoist_credentials["email"],
                  todoist_credentials["password"])

    if not session.authenticated:
        session.auth(lectio_credentials["username"],
                     lectio_credentials["password"])

    logger.info("Getting Lectio assignments.")
    assignments = session.get_assignments()

    service.sync(resource_types=["projects", "items"])

    # clear all items
    logger.info("Clearing assignments project on Todoist.")
    for item in service.items.all():
        if item["project_id"] == PROJECT_ID:
            logger.info("Deleting item '{}'' with id: '{}'"
                        .format(item["content"], item["id"]))
            item.delete()

    logger.info("Commiting changes to Todoist.")
    service.commit()

    for assignment in assignments:
        if assignment.status == AssignmentStatuses.HANDED_IN:
            continue

        time = assignment.deadline.astimezone(TIMEZONE)
        time_as_str = time.strftime("%d %B %Y %H:%M")

        logger.info("Adding item '{}' to assignments project on Todoist, "
                    "due: '{}'".format(assignment.title, time_as_str))
        service.items.add(assignment.title, PROJECT_ID,
                          date_string=time_as_str, date_lang="en")

    logger.info("Commiting changes to Todoist.")
    service.commit()


def main():
    """
    Exports Lectio to Google Calendar and Todoist.
    """
    session = Session(SCHOOL_ID, tz=TIMEZONE)

    database = Database()
    database.connect()

    if GOOGLE_ENABLED:
        main_google(session, database)

    if TODOIST_ENABLED:
        main_todoist(session)


if __name__ == '__main__':
    main()
