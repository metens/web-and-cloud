import sqlite3

class Model():
    def select(self):
        self.connection = sqlite3.connect("DB_FILE")
        self.cursor = self.connection.cursor()
        pass

    def insert(self):
        pass