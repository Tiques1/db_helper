import socket
import usermessages
import authentication as auth


class Postgres:
    def __init__(self, dbname: str, user: str, password: str, addr: str = 'localhost', port: int = 5432):
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

            msg = usermessages.startup_message(user=self.user, database=self.dbname)
            self.__sock.send(msg)
            rcv = self.__sock.recv(4096)

            resp = rcv.decode(encoding='utf-8', errors='ignore')[0]
            msg_len = int.from_bytes(rcv[1:5], byteorder='big', signed=False)
            specifier = int.from_bytes(rcv[5:9], byteorder='big', signed=False)

            authenticator = auth.HANDLER.get((resp, msg_len, specifier))
            authenticator(rcv, self.__sock)

        except socket.error as e:
            print(e)

    def query(self, text):
        self.__sock.send(usermessages.query(text))
        return self.__sock.recv(4096)

    def disconnect(self):
        try:
            self.__sock.close()
        except socket.error as e:
            print(e)

    def __del__(self):
        self.disconnect()


def main():
    db = Postgres('dmx', 'postgres', '1111')
    db.connect()
    result = db.query('SELECT * FROM cities WHERE population < 10000 order by population')
    print(result)
    print(result.decode('utf-8', errors='ignore'))
    db.disconnect()


if __name__ == "__main__":
    main()
