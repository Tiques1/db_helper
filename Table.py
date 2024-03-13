class Table:
    def __init__(self, connection):
        self.__rows = []
        self.__conn = connection

    @staticmethod
    def _create(name, header, postgres):
        query = f'CREATE TABLE {name} ('
        for i in header:
            query += i + ' ' + str(header[i]) + ',\n'
        query = query[:-2] + ')'
        print(query)
        postgres.query(query)

    def insert(self, rows):
        pass

    def print(self):
        print(self.__rows)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        query = f'ALTER TABLE {self.__name} RENAME TO {value};'
        self.__postgres.query(query)
        self.__name = value

    def __iter__(self):
        self.__pointer = 0
        return self

    def __next__(self):
        if self.__pointer < len(self.__header):
            self.__pointer += 1
            return self.__header[self.__pointer-1]
        else:
            raise StopIteration


class Field:
    types = {
        int: 'INTEGER',
        str: 'VARCHAR',
        bool: 'BOOLEAN'
    }

    def __init__(self, dtype, length):
        self.length = length
        self.type = dtype

    def __str__(self):
        field = self.types.get(self.type)
        if self.type not in (int, bool):
            field += f'({self.length})'
        return field
