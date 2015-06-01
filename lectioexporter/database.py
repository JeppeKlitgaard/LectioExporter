import sqlite3

from .config import DATABASE_LOCATION, PERIODS_TABLE_NAME


class Database(object):
    def __init__(self):
        self.connection = None
        self.cursor = None

    def assert_connected(self):
        """
        Ensures the database is connected.
        """
        assert(self.connection is not None)

    def connect(self):
        """
        Connects to the SQLite3 database.
        """
        self.connection = sqlite3.connect(DATABASE_LOCATION)
        self.cursor = self.connection.cursor()

        self._create_periods_if_not_exists()

        return True

    def _create_periods_if_not_exists(self):
        self.assert_connected()

        sql = """
        CREATE TABLE IF NOT EXISTS {} (
            id INTEGER primary key autoincrement not null,
            PeriodID TEXT unique,
            PeriodHash TEXT);
        """
        sql = sql.format(PERIODS_TABLE_NAME)
        self.cursor.executescript(sql)

        self.connection.commit()

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self):
        self.assert_connected()

        sql = "SELECT count(*) FROM {}".format(PERIODS_TABLE_NAME)
        self.cursor.execute(sql)

        result = self.cursor.fetchone()

        return result[0]

    def __getitem__(self, key):
        self.assert_connected()

        sql = "SELECT PeriodHash from {} WHERE PeriodID=(?)"
        sql = sql.format(PERIODS_TABLE_NAME)

        self.cursor.execute(sql, (key,))

        result = self.cursor.fetchall()

        if not result:
            raise KeyError("Key not found.")

        return result[0][0]

    def __setitem__(self, key, value):
        self.assert_connected()

        sql = "INSERT INTO {} (PeriodID, PeriodHash) VALUES (?, ?)"
        sql = sql.format(PERIODS_TABLE_NAME)

        self.cursor.execute(sql, (key, value))

        self.connection.commit()

    def __delitem__(self, key):
        self.assert_connected()

        sql = "DELETE FROM {} WHERE PeriodID=(?)"
        sql = sql.format(PERIODS_TABLE_NAME)

        self.cursor.execute(sql, (key,))

        self.connection.commit()

    def __contains__(self, item):
        self.assert_connected()

        try:
            self[item]
        except KeyError:
            return False
        return True
