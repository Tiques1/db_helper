import socket
import struct
import client_messages as clms
import authentication as auth
import query


class Postgres:
    def __init__(self, dbname: str, user: str, password: str, addr: str = 'localhost', port: int = 5432):
        self.__sock = None
        self.dbname = dbname
        self.user = user
        self.password = password
        self.addr = addr
        self.port = port
        self._params = {}
        self.__back_keys = {}

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.addr, self.port))

            msg = clms.startup_message(user=self.user, database=self.dbname)
            self.__sock.send(msg)

            rcv = reciever(self.__sock)
            self._params, self.__back_keys = auth.handler(rcv, self.__sock)
        except socket.error as e:
            print(e)

    def query(self, text):
        self.__sock.send(clms.query(text))
        rcv = reciever(self.__sock)
        query.handler(rcv)

    def disconnect(self):
        self.__sock.send(clms.terminate())
        try:
            self.__sock.close()
            print('Disconnected')
        except socket.error as e:
            print(e)

    def __explore(self):
        pass

    def __del__(self):
        try:
            self.__sock.close()
        except OSError:
            pass


def reciever(sock: socket) -> [bytes]:
    requests = []
    sock.settimeout(1)
    try:
        while True:
            b = sock.recv(5)
            length = struct.unpack('!I', b[1:])[0]
            requests.append(b + sock.recv(length-4))
    except socket.timeout:
        pass
    return requests


def main():
    db = Postgres('dmx', 'postgres', '1111')
    db.connect()
    # db.query('')
    # print(res)
    # [print(result.decode('utf-8', errors='ignore')) for result in res]
    db.disconnect()


if __name__ == "__main__":
    main()
