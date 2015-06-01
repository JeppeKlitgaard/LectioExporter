from lectioexporter.google_calendar import clear_calendar
from lectioexporter.google_calendar import make_service
from lectioexporter.credentials import get_google_credentials
from lectioexporter.config import CALENDAR_ID

from datetime import datetime
import pytz

credentials = get_google_credentials()
service = make_service(credentials)

clear_calendar(service, CALENDAR_ID)
