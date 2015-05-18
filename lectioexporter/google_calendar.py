import os
import argparse
from datetime import datetime, timedelta
import pytz
from time import sleep
from pprint import pprint
import json

import oauth2client
from oauth2client import client, tools
from oauth2client import file as oa2c_file

from googleapiclient.discovery import build
from googleapiclient import errors

from httplib2 import Http

from .utilities import rfc33392dt, dt2rfc3339

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "LectioExporter"


def get_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    parent_parsers = [tools.argparser]
    parser = argparse.ArgumentParser(
        description=APPLICATION_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)

    flags = parser.parse_args()

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".credentials")

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   APPLICATION_NAME + ".json")

    store = oa2c_file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

    return credentials


def make_service(credentials):
    """
    Makes a ``service`` object based on ``credentials``.
    """
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
        print("Delete")
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

    event_result = service.events().insert(calendarId=calendarId,
                                           fields=",".join(fields.keys()),
                                           body=fields).execute()

    return event_result


def main():
    credentials = get_credentials()
    service = make_service(credentials)

    now = datetime.utcnow()
    then = datetime(2015, 5, 13, 17, 18, 9)

    print(dt2rfc3339(now))
    print(dt2rfc3339(then))
    print(json.dumps(list_calendars(service), indent=2))

    #print(create_event(service, "jeppe@dapj.dk", "Summary!!", "confirmed", "N7", "Description goes here!",
    #                   now, then))


if __name__ == "__main__":
    main()
