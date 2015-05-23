from distutils.core import setup
import lectioexporter
import sys

if (3, 0) > sys.version_info:
    sys.exit("Please use python3.")

setup(name="lectioexporter",
      version=".".join([str(x) for x in lectioexporter.__version__]),
      description="Exports your Lectio timetable and assignments to "
                  "Google Calendar and Todoist.",
      author="Jeppe Klitgaard",
      author_email="jeppe@dapj.dk",
      packages=["lectioexporter"],
      scripts=[])
