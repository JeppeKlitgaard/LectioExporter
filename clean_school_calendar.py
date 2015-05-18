from lectioexporter.google_calendar import clear_calendar
from lectioexporter.google_calendar import get_credentials, make_service
from lectioexporter.config import CALENDAR_ID

from datetime import datetime
import pytz

credentials = get_credentials()
service = make_service(credentials)

min_time = datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC)

clear_calendar(service, CALENDAR_ID, min_time=min_time)
