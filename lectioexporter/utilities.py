from datetime import datetime


def dt2rfc3339(dt):
    return dt.isoformat() + "Z"


def rfc33392dt(string):
    string = string.replace(":", "")  # Hacky fix for %z
    fmt = r"%Y-%m-%dT%H%M%S%z"

    return datetime.strptime(string, fmt)
