import socket
import struct

def query(sock, string):
    message = b'Q' + struct.pack('!I', len(string) + 5) + string.encode(encoding='utf-8') + b'\x00'
    print(message)
    sock.send(message)

def send_message(sock, message):
    message_length = struct.pack('!I', len(message) + 4)
    sock.send(message_length + message)

def receive_message(sock):
    message_length = struct.unpack('!I', sock.recv(4))[0] - 4
    message = sock.recv(message_length)
    return message

def build_startup_message(database, user):
    # Сообщение старта соединения PostgreSQL
    # См. https://www.postgresql.org/docs/current/protocol-message-formats.html
    null_byte = b'\x00'
    startup_message = struct.pack('!H', 3) + b'\x00\x00' + null_byte.join([b'database', database.encode(), b'user', user.encode(), b'\x00'])
    return startup_message

def main():
    # Параметры подключения
    database = "dmx"
    user = "postgres"
    password = "1111"

    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаемся к сокету PostgreSQL
    try:
        sock.connect(("localhost", 5432))

        # Отправляем сообщение старта соединения
        message = build_startup_message(database, user)
        send_message(sock, message)

        # Ожидаем ответ на стартовое сообщение
        response = receive_message(sock)
        print(response)
        print("Ответ на стартовое сообщение:", response.decode(encoding='cp1251'))

        # Пример SQL-запроса
        message = "SELECT num FROM house;"
        query(sock, message)

        # Получение ответа
        response = receive_message(sock)
        print("Ответ на SQL-запрос:", response.decode('utf-8', errors='ignore'))

    except socket.error as e:
        print(f"Ошибка соединения с PostgreSQL: {e}")

    finally:
        # Закрытие сокета
        sock.close()

if __name__ == "__main__":
    main()
