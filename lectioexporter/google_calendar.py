import os
import argparse
from datetime import datetime

import oauth2client
from oauth2client import client, tools
from oauth2client import file as oa2c_file

from googleapiclient.discovery import build
from googleapiclient import errors

from httplib2 import Http

SCOPES = "https://www.googleapis.com/auth/calendar.readonly"
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "Calendar API Quickstart"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    parent_parsers = [tools.argparser]
    parser = argparse.ArgumentParser(
        description="Calendar Api",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)

    flags = parser.parse_args()

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'calendar-api-quickstart.json')

    store = oa2c_file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

    return credentials


def main():
    credentials = get_credentials()
    service = build("calendar", "v3", http=credentials.authorize(Http()))

    now = datetime.utcnow().isoformat() + "Z"

    try:
        events_result = service.events().list(calendarId="jeppe@dapj.dk").execute()
    except errors.HttpError as e:
        print(e)

    print(events_result)


if __name__ == '__main__':
    main()
