import re


class Column:
    def __init__(self, table, connection, name: str, dtype: str, not_null=0, default='', primary_key=0):
        self.__name = name
        self.__conn = connection
        self.__table = table
        self.__type = dtype
        self.__not_null = not_null
        self.__default = default
        self.__primary_key = primary_key

    def __call__(self, *args, **kwargs):
        query = f'SELECT {self.__name} FROM {self.__table.name()} WHERE '
        while kwargs:
            item = kwargs.popitem()
            if item[0] not in self.__table.__dict__:
                continue
            query += f'{item[0]} = {item[1]}, '
        query = re.sub(', $', ' ', query) + ';'
        return self.__conn.query(query)

    def name(self):
        return self.__name

    def column_info(self):
        return self.__name, self.__type, self.__not_null, self.__default, self.__primary_key

    def rename(self, name):
        pass

    def delete(self):
        pass

    def set(self, value):
        pass
