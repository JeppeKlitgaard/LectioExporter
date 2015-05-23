from getpass import getpass
import todoist

api = todoist.TodoistAPI()

username = input("Todoist username: ")
password = getpass("Todoist password: ")

api.login(username, password)

api.sync(resource_types=["projects"])

for project in api.projects.all():
    print("{}: {}".format(project["name"], project["id"]))
