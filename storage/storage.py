import os
import sqlite3
import sys


class Storage:

    def __init__(self):
        self.file_name = "./database.sql"
        self.__conn = None
        self.__tries = 0
        self.__maxTries = 3

    @property
    def connection(self):
        if self.__conn is None:
            if self.__tries == self.__maxTries:
                sys.exit("Error trying to open connection into sqlite.")

            self.__tries += 1
            self.start_connection()
            return self.connection
        else:
            return self.__conn

    def start_connection(self):
        if not os.path.isfile(self.file_name):
            self.create_file()

        self.__conn = sqlite3.connect(self.file_name)
        print("SQLite Database successfully connected with version {}!".format(sqlite3.version))

    def create_file(self):
        os.mknod(self.file_name)
