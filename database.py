from table import Table


class Database:
    def __init__(self, connection):
        self.__conn = connection

    def update(self):
        pass

    def create(self, name):
        self.__conn.query(f'CREATE TABLE {name}()')
        self.__dict__[name] = Table(self.__conn, name)

    def tables(self):
        tables = []
        for i in self.__dict__:
            if isinstance(i, Table):
                tables.append(i)
        return tables


class PostgreSQL(Database):
    def update(self):
        table = self.__conn.query('SELECT * FROM pg_catalog.pg_tables WHERE schemaname = \'public\';')
        self.__dict__[table.table_name] = Table(self.__conn)


class SQLite(Database):
    def update(self):
        pass


class SQLAlchemy(Database):
    def update(self):
        pass
