# LectioExporter
Exports Lectio timetable and assignments to Google Calendar and Todoist

## Background
`Lectio` is a school all-in-one system used by Danish highschools, but sadly has no api nor ability to export data.

This project uses my other project, `pylectio` and Google's Python API and Todoist's Python API
to export data from Lectio to Google Calendar and Todoist.

It will only work for me, but with some tinkering in `config.py`, anyone should be able to use it.

## Installation
Only works with `Python 3`

Ensure you are the user that you want to have the crontab installed on.

`pip install -r requirements.txt`

`python setup.py install`

`configure_lectioexporter`

`export_lectio`

## Contact
If want to use this yourself but can't get it to work, please don't hesitate to contact me:

Email: [jeppe@dapj.dk](mailto:jeppe@dapj.dk)
