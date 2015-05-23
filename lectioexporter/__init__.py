"""
Exports your lectio timetable to a Google Calendar and your
lectio assignments to Todoist.
"""
__version__ = (0, 1, 1)

import logging
from .config import LOGGING_LEVEL

logger = logging.getLogger("LectioExporter")

logger.setLevel(LOGGING_LEVEL)

fmt_str = "[%(name)s: %(levelname)s] %(message)s"
formatter = logging.Formatter(fmt_str)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
