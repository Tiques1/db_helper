import re
import numpy
from column import Column
from multipledispatch import dispatch


class Table:
    def __init__(self, connection, name):
        self.__conn = connection
        self.__name = name

    @dispatch()
    def name(self):
        return self.__name

    @dispatch()
    def columns(self):
        columns = []
        for i in self.__dict__:
            if isinstance(i, Table):
                columns.append(i)
        return columns

    @dispatch(str)
    def rename(self, name):
        self.__conn.query(f'ALTER TABLE {self.__name} RENAME TO {name};')
        del self.__conn.database[self.__name]
        self.__name = name
        self.__conn.database[self.__name] = self

    @dispatch()
    def delete(self):
        self.__conn.query(f'DROP TABLE {self.__name};')
        del self.__conn.database[self.__name]

    @dispatch(tuple)
    def insert(self, rows):
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
        query = f'ALTER TABLE {self.__name} ADD {column_name} {dtype};'
        self.__conn.query(query)
        self.__dict__[column_name] = Column(self, self.__conn, column_name, dtype)
