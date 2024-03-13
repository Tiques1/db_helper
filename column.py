import re


class Column:
    def __init__(self, table, connection, name, dtype, not_null=False, default='', primary_key=False, foreign_key=''):
        self.__name = name
        self.__conn = connection
        self.__table = table
        self.__type = dtype
        self.__not_null = not_null
        self.__default = default
        self.__primary_key = primary_key
        self.__foreign_key = foreign_key  # table (column)

    def __call__(self, *args, **kwargs):
        query = f'SELECT {self.__name} FROM {self.__table.name()} WHERE '
        while kwargs:
            item = kwargs.popitem()
            if item[0] not in self.__table.__dict__:
                continue
            query += f'{item[0]} = {item[1]}, '
        query = re.sub(', $', ' ', query) + ';'
        return self.__conn.query(query)

    def rename(self, name):
        pass

    def delete(self):
        pass

    def set(self, value):
        pass
