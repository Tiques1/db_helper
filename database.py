import table
from table import Table


class Database:
    def __init__(self, connection):
        self.conn = connection
        self.update()

    def update(self):
        pass

    # def create(self, name):
    #     self.conn.query(f'CREATE TABLE {name} ( );')
    #     self.__dict__[name] = Table(self.conn, name, True)

    def tables(self):
        tables = []
        for i in self.__dict__.values():
            if isinstance(i, table.Table):
                tables.append(i)
        return tables


class PostgreSQLDB(Database):
    def update(self):
        t = self.conn.query('SELECT * FROM pg_catalog.pg_tables WHERE schemaname = \'public\';')
        self.__dict__[t.table_name] = Table(self.conn, '', True)


class SQLiteDB(Database):
    def update(self):
        tables = self.conn.query('SELECT * FROM sqlite_master where type=\'table\';')
        while tables.row(True):
            t = tables.rows()[-1]
            self.__dict__[t[1]] = Table(self.conn, t[1], True)


class SQLAlchemyDB(Database):
    def update(self):
        pass
