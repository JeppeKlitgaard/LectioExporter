import json

from .config import DATABASE_LOCATION


class Database(object):
    def __init__(self):
        self.filepath = DATABASE_LOCATION
        self.data = dict()

    def load(self, safe=True):
        try:
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError as e:
            if safe:
                print("Failed to load DB.")
            else:
                raise e

    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, item):
        return item in self.data
