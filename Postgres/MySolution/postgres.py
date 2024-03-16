import socket
import struct
from Postgres import authentication as auth, client_messages as clms
from Postgres import query
import database


class Postgres:
    def __getitem__(self, item):
        return getattr(self, item)

    def __init__(self, dbname: str, user: str, password: str, addr: str = 'localhost', port: int = 5432):
        self.__sock = None
        self.dbname = dbname
        self.user = user
        self.password = password
        self.addr = addr
        self.port = port
        self.__params = {}
        self.__back_keys = {}
        self.__database = database.Database(self)

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.addr, self.port))

            msg = clms.startup_message(user=self.user, database=self.dbname)
            self.__sock.send(msg)

            rcv = self.__reciever(self)
            self.__params, self.__back_keys = auth.handler(rcv, self.__sock)
        except socket.error:
            pass

    def query(self, text):
        self.__sock.send(clms.query(text))
        rcv = self.__reciever(self)
        return query.handler(rcv, self)

    def disconnect(self):
        self.__sock.send(clms.terminate())
        try:
            self.__sock.close()
        except socket.error:
            pass

    def database(self):
        return self.__database

    @property
    def params(self):
        param = {key.decode('utf-8', errors='ignore'):
                 value.decode('utf-8', errors='ignore') for key, value in self.__params.items()}
        return param

    @staticmethod
    def __reciever(self) -> [bytes]:
        requests = []
        self.__sock.settimeout(1)
        try:
            while True:
                b = self.__sock.recv(5)
                length = struct.unpack('!I', b[1:])[0]
                requests.append(b + self.__sock.recv(length-4))
        except socket.timeout:
            pass
        return requests
