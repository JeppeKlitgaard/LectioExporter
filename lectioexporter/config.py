"""
Contains configuration options and values used by LectioExporter.
"""

import re
import os
import pytz

import logging

LOGGING_LEVEL = logging.DEBUG

CONFIG_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"),
                                          ".lectioexporter"))

TIMEZONE = pytz.timezone("Europe/Copenhagen")

GOOGLE_ENABLED = True
EVERNOTE_ENABLED = False

# Database
DATABASE_LOCATION = os.path.join(CONFIG_DIR, "lectioexporter_db.json")

# Google
SCOPES = ("https://www.googleapis.com/auth/calendar",
          "https://www.googleapis.com/auth/calendar.readonly",
          "https://www.googleapis.com/auth/userinfo.email")

CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = "LectioExporter"

CALENDAR_ID = "dapj.dk_oc1tppk1qrfglv9f2u6igpqetg@group.calendar.google.com"

# Evernote
EVERNOTE_DEV_TOKEN_FILE = os.path.join(CONFIG_DIR, "evernote_dev.token")
EVERNOTE_NOTEBOOK_GUID = "8ae69883-89dd-4d04-a7c3-4c866a27e7b6"
EVERNOTE_ASSIGNMENT_PREFIX = "SG Opgave: "
EVERNOTE_HOMEWORK_PREFIX = "SG Lektie: "

# Lectio
SCHOOL_ID = "248"
STUDENT_ID = "9232029391"
WEEKS_TO_CHECK = 6

LOOKUP_TEACHERS = {
    "BJ": "Bente",
    "JLI": "Jens",
    "FG": "Flemming",
    "JE": "Klaus",
    "LST": "Lea",
    "LK": "Louise",
    "LJN": "Louise",
    "MS": "Maja",
    "MG": "Mette",
    "MOE": "Michael",
}

LOOKUP_GROUPS = {
    re.compile(r".*1 me11$", re.I): "Mediefag",
    re.compile(r".*1cmxy id2$", re.I): "Idræt",
    re.compile(r".*bi$", re.I): "Biologi",
    re.compile(r".*da$", re.I): "Dansk",
    re.compile(r".*en$", re.I): "Engelsk",
    re.compile(r".*fy$", re.I): "Fysik",
    re.compile(r".*hi$", re.I): "Historie",
    re.compile(r".*ke$", re.I): "Kemi",
    re.compile(r".*ma$", re.I): "Matematik",
    re.compile(r".*sa$", re.I): "Samfundsfag",
    re.compile(r".*ty$", re.I): "Tysk",
    re.compile(r".*klassens time$"): "Klassens time",
    re.compile(r"^Skr\. arb\..*"): "Skriftligt arbejde",
}
