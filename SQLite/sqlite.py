import re
import sqlite3
from database import SQLiteDB
from table import Table


class SQLite:
    def __init__(self, database):
        self.__conn = sqlite3.connect(database)
        self.__cursor = self.__conn.cursor()
        self.__database = SQLiteDB(self)

    # Take query or filename.sql
    def query(self, query: str):
        if query == re.match('.*\.sql', query):
            with open(query, 'r+') as file:
                text = '\n'.join(file.readlines())
                response = self.__cursor.executescript(text)
        else:
            response = self.__cursor.execute(query)
        self.__conn.commit()
        table = Table(self, '', natural=False)
        table.handle(response, self.__cursor.description)
        return table

    def disconnect(self):
        self.__conn.close()

    def database(self):
        return self.__database
