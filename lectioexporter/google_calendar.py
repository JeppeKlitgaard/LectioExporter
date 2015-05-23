"""
Contains functions and classes used to interact with Google Calendar.
"""

from datetime import datetime, timedelta
import pytz

from googleapiclient.discovery import build

from httplib2 import Http

import logging

from .utilities import dt2rfc3339


logger = logging.getLogger("LectioExporter")


def make_service(credentials):
    """
    Makes a ``service`` object based on ``credentials``.
    """
    logger.info("Making Google service.")
    service = build("calendar", "v3", http=credentials.authorize(Http()))

    return service


def list_calendars(service):
    """
    Lists all calendars connected to ``service``.
    """
    result = service.calendarList().list().execute()

    return result


def clear_calendar(service, calendarId, max_results=2500, min_time=None):
    """
    When ``min_time`` is ``None``, the ``min_time`` will be in one hour.
    """
    logger.info("Clearing calendar: {}".format(calendarId))

    if min_time is None:
        min_time = datetime.utcnow() + timedelta(hours=1)
        min_time = min_time.replace(tzinfo=pytz.UTC)

    events = []
    next_page_token = ""
    while True:
        kwargs = {
            "calendarId": calendarId,
            "maxResults": max_results,
            "timeMin": dt2rfc3339(min_time),
            "singleEvents": "true",
            "orderBy": "startTime"
        }
        if next_page_token:
            kwargs["pageToken"] = next_page_token

        events_result = service.events().list(**kwargs).execute()

        events.extend(events_result["items"])

        if "nextPageToken" in events_result:
            next_page_token = events_result["nextPageToken"]
        else:
            break

    for event in events:
        fmt = "Deleting event '{}' with id: '{}' on calendar with id: '{}'"
        logger.info(fmt.format(event["summary"], event["id"], calendarId))
        service.events().delete(calendarId=calendarId,
                                eventId=event["id"]).execute()

    return True


def create_event(service, calendarId, summary, status, location, description,
                 start_time, end_time):
    """
    Creates an event on the given calendar using given service.
    """
    fields = {
        "summary": summary,
        "status": status,
        "location": location,
        "description": description,
        "start": {
            "dateTime": dt2rfc3339(start_time)  # Google wants RFC 3339 format
        },
        "end": {
            "dateTime": dt2rfc3339(end_time)
        }
    }

    logger.info("Creating event '{}' on calendar with id: '{}'"
                .format(fields["summary"], calendarId))

    event_result = service.events().insert(calendarId=calendarId,
                                           fields=",".join(fields.keys()),
                                           body=fields).execute()

    return event_result
