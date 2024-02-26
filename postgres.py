import socket


class Postgres:
    def __init__(self, dbname: str, user: str, password: str, addr: str = 'localhost', port: str = '5432'):
        self.__sock = None
        self.dbname = dbname
        self.user = user
        self.password = password
        self.addr = addr
        self.port = port

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.addr, self.port))
        except socket.error as e:
            print(e)

    def query(self):
        pass

    def disconnect(self):
        try:
            self.__sock.close()
        except socket.error as e:
            print(e)

    def __del__(self):
        self.disconnect()
