import re

SCHOOL_ID = "248"
STUDENT_ID = "9232029391"
WEEKS_TO_CHECK = 3
CALENDAR_ID = "dapj.dk_oc1tppk1qrfglv9f2u6igpqetg@group.calendar.google.com"

LOOKUP_TEACHERS = {
    "BJ": "Bente",
    "JDM": "Jakúp",
    "JLI": "Jens",
    "FG": "Flemming",
    "JE": "Klaus",
    "LI": "Morten",
    "TVL": "Teresa",
    "LST": "Lea",
    "LK": "Louise"
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
