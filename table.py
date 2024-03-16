import re
import numpy

import column
from column import Column
from multipledispatch import dispatch


class Table:
    def __init__(self, connection,  # It is one of Posgres, SQLite or other class
                 name: str,
                 natural: bool):  # True if table actually exists in table. Defined automatically
        self.__conn = connection
        self.__name = name
        self.__rows = []
        self.__natural = natural
        self.__response = None
        if self.__natural:
            self.update()

    def name(self):
        return self.__name

    def columns(self):
        tables = []
        for i in self.__dict__.values():
            if isinstance(i, column.Column):
                tables.append(i)
        return tables

    def rename(self, name: str):
        if self.__natural:
            self.__conn.query(f'ALTER TABLE {self.__name} RENAME TO {name};')
        del self.__conn.database[self.__name]
        self.__name = name
        self.__conn.database[self.__name] = self

    def delete(self):
        if self.__natural:
            self.__conn.query(f'DROP TABLE {self.__name};')
        del self.__conn.database[self.__name]

    def insert(self, rows):  # rows must be 2-dimensional array
        if not self.__natural:
            for i in rows:
                self.__rows = numpy.append(self.__rows, i)
            return
        rows = numpy.array(rows)
        if not rows.ndim == 2:
            return
        query = f'INSERT INTO {self.__name} VALUES '
        for i in rows:
            query += '('
            for j in i:
                query += str(j) + ', '
            query = re.sub(', $', ' ', query) + '), '
        query = re.sub(', $', ' ', query) + ';'
        self.__conn.query(query)

    # It is possible add complex logic to alter table query
    def add(self, column_name: str, dtype: str, not_null: bool = False,
            default: str = '', primary_key: bool = False, foreign_key: str = ''):
        if self.__natural:
            query = f'ALTER TABLE {self.__name} ADD {column_name} {dtype};'
            self.__conn.query(query)
        self.__dict__[column_name] = Column(self, self.__conn, column_name, dtype)

    def handle(self, response, description):  # description = cursor.description
        if description:
            headers = [i[0] for i in description]
            for i in headers:
                self.__dict__[i] = Column(self, self.__conn, i, 'str')
        self.__response = response

    def row(self, append=False):
        row = self.__response.fetchone()
        if append:
            self.__rows.append(row)
        return row

    def rows(self):
        return self.__rows

    def natural(self):
        return self.__natural

    def update(self):
        table = self.__conn.query(f'PRAGMA table_info(\'{self.__name}\')')
        while table.row(True):
            row = table.rows()[-1]
            self.__dict__[row[1]] = Column(self, self.__conn, row[1], row[2],
                                           row[3], row[4], row[5])
