import struct
import client_messages as clms
import query

"""
Types of authentication
https://www.postgresql.org/docs/current/protocol-message-formats.html
"""
HANDLER = {
    ('E', None, None): lambda rcv, sock: query.error_response(rcv[0]),
    ('R', 8, 0): lambda rcv, sock: authentication_ok(rcv),
    ('R', 8, 2): lambda rcv, sock: authentication_kerberos_v5(rcv, sock),
    ('R', 8, 3): lambda rcv, sock: authentication_cleartext_password(rcv, sock),
    ('R', 12, 5): lambda rcv, sock: authentication_md5_password(rcv, sock),
    ('R', 8, 7): lambda rcv, sock: authentication_gss(rcv, sock),
    ('R', 8, 9): lambda rcv, sock: authentication_sspi(rcv, sock),
    ('R', None, 10): lambda rcv, sock: authentication_sasl(rcv, sock),
    ('v', None, None): lambda rcv, sock: negotiate_protocol_version(rcv, sock)
}

"""
Every auth function finally call authentication_ok,
which return connection __params and backend keys.
Params and backend keys returned by authentication_ok 
return back to handler.
Handler return them to Postgres class

Call tree
Postgres.connection -> authentication.handler -> func -> authentication_ok
"""


def handler(rcv: [bytes], sock) -> [{}, {}]:
    resp = rcv[0].decode(encoding='utf-8', errors='ignore')[0]
    msg_len = struct.unpack('!I', rcv[0][1:5])[0]
    specifier = struct.unpack('!I', rcv[0][5:9])[0]
    authenticator = HANDLER.get((resp, msg_len, specifier))
    return authenticator(rcv, sock)


def authentication_ok(rcv: [bytes]):
    print('Authentication ok')
    params = {}
    back_keys = {}
    msg_types = {
        'E': lambda msg: query.error_response(msg),
        'S': lambda msg: params.update({msg[5:].split(b'\x00')[0]: msg[5:].split(b'\x00')[1]}),
        'K': lambda msg: back_keys.update({'process_id': msg[5:9], 'secret_key': msg[9:]}),
        'Z': lambda msg: query.ready_for_query(msg),
        'N': lambda msg: query.notice_response(msg)
    }
    for i in rcv:
        func = msg_types.get(i.decode('utf-8', errors='ignore')[0])
        if func:
            func(i)

    return params, back_keys


def authentication_kerberos_v5(rcv, sock):
    return authentication_ok(rcv)


def authentication_cleartext_password(rcv, sock):
    return authentication_ok(rcv)


def authentication_md5_password(rcv, sock):
    return authentication_ok(rcv)


def authentication_gss(rcv, sock):
    return authentication_ok(rcv)


def authentication_sspi(rcv, sock):
    return authentication_ok(rcv)


def authentication_sasl(rcv, sock):
    return authentication_ok(rcv)


def negotiate_protocol_version(rcv, sock):
    return authentication_ok(rcv)
