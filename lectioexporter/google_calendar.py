import os
import argparse
from datetime import datetime, time
from pprint import pprint
import json

import oauth2client
from oauth2client import client, tools
from oauth2client import file as oa2c_file

from googleapiclient.discovery import build
from googleapiclient import errors

from httplib2 import Http

SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "LectioExporter"


def dt2rfc3339(dt):
    return dt.isoformat() + "Z"


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
    service = build("calendar", "v3", http=credentials.authorize(Http()))

    now = datetime.utcnow()
    then = datetime(2015, 5, 13, 17, 18, 9)

    print(dt2rfc3339(now))
    print(dt2rfc3339(then))

    print(create_event(service, "jeppe@dapj.dk", "Summary!!", "confirmed", "N7", "Description goes here!",
                       now, then))


if __name__ == "__main__":
    main()
