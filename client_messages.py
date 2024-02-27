import struct

NULL_BYTE = b'\x00'

"""All these functions take str and return bytes"""


def bind():
    pass


def close():
    pass


def copy_data():
    pass


def copy_done():
    pass


def copy_fail():
    pass


def describe():
    pass


def execute():
    pass


def flush():
    pass


def function_call():
    pass


def gssenc_request():
    pass


def gss_response():
    pass


def parse():
    pass


def password_message():
    pass


def query(string):
    return b'Q' + struct.pack('!I', len(string) + 5) + string.encode(encoding='utf-8') + b'\x00'


def sasl_initial_response():
    pass


def sasl_response():
    pass


def ssl_request():
    pass


def startup_message(database, user):
    message = NULL_BYTE.join(
        [b'database', database.encode(), b'user', user.encode(), b'\x00'])
    return struct.pack('!I', len(message) + 8) + struct.pack('!H', 3) + b'\x00\x00' + message


def sync():
    pass


def terminate():
    pass
