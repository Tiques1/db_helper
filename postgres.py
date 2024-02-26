import socket
import authentification
import usermessages
import struct


class Postgres:
    def __init__(self, dbname: str, user: str, password: str, addr: str = 'localhost', port: int = 5432):
        self.__sock = None
        self.dbname = dbname
        self.user = user
        self.password = password
        self.addr = addr
        self.port = port
        self.options = {}
        self.__backend = {'process_id': '', 'secret_key': ''}
        self.__handlers = {
            ('E', None, None): lambda rcv: print('Error', rcv.decode('utf-8', errors='ignore')),
            ('R', 8, 0): lambda rcv: None,  # AuthentificationOk
            ('R', 8, 2): lambda rcv: None,  # AuthenticationKerberosV5
            ('R', 8, 3): lambda rcv: None,  # AuthenticationCleartextPassword
            ('R', 12, 5): lambda rcv: None,  # AuthenticationMD5Password
            ('R', 8, 7): lambda rcv: None,  # AuthenticationGSS
            ('R', 8, 9): lambda rcv: None,  # AuthenticationSSPI
            ('R', None, 10): lambda rcv: None,  # AuthenticationSASL
            ('v', None, None): lambda rcv: None  # NegotiateProtocolVersion
        }

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect((self.addr, self.port))

            msg = usermessages.startup_message(user=self.user, database=self.dbname)
            self.__sock.send(msg)

            rcv = self.__sock.recv(4096)
            resp = rcv.decode(encoding='utf-8', errors='ignore')[0]

            print(rcv)
            print(rcv.decode('utf-8', errors='ignore'))

            msg_len = int.from_bytes(rcv[1:5], byteorder='big', signed=False)
            specifier = int.from_bytes(rcv[6:10], byteorder='big', signed=False)

            """
            Next find out what a version auth protocol server requested
            https://www.postgresql.org/docs/current/protocol-message-formats.html
            """

            auth_method = self.__handlers.get((resp, msg_len, specifier))
            if auth_method:
                auth_method(rcv)

            i = 9
            message = rcv.decode('utf-8', errors='ignore')
            while i <= len(message) - 1:
                if message[i] == 'S' or message[i] == 'K':
                    length = int.from_bytes(rcv[i + 1:i + 5], byteorder='big', signed=False)
                    if message[i] == 'S':
                        key, value = message[i + 5:i + length + 1].split('\x00')[:2]
                        self.options[key] = value
                    elif message[i] == 'K':
                        self.__backend['process_id'] = message[i + 5:i + 9]
                        self.__backend['secret_key'] = message[i + 9:i + 13]
                    i += length + 1
                elif message[i] == 'N' or message[i] == 'E':
                    length = int.from_bytes(rcv[i + 1:i + 5], byteorder='big', signed=False)
                    print(message[i + 5:i + length])
                    i += length + 1
                elif message[i] == 'Z':
                    print('Ready for query')
                    break
                else:
                    i += 1

            print(self.__backend, self.options)

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


db = Postgres('dmx', 'postgres', '1111')
db.connect()
