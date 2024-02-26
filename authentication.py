HANDLER = {
    ('E', None, None): lambda rcv, sock: error_response(rcv, sock),
    ('R', 8, 0): lambda rcv, sock: authentication_ok(rcv, sock),
    ('R', 8, 2): lambda rcv, sock: authentication_kerberos_v5(rcv, sock),
    ('R', 8, 3): lambda rcv, sock: authentication_cleartext_password(rcv, sock),
    ('R', 12, 5): lambda rcv, sock: authentication_md5_password(rcv, sock),
    ('R', 8, 7): lambda rcv, sock: authentication_gss(rcv, sock),
    ('R', 8, 9): lambda rcv, sock: authentication_sspi(rcv, sock),
    ('R', None, 10): lambda rcv, sock: authentication_sasl(rcv, sock),
    ('v', None, None): lambda rcv, sock: negotiate_protocol_version(rcv, sock)
}


def error_response(rcv, sock):
    if rcv.decode('utf-8', errors='ignore')[9] == 'E':
        print('ConnectionError')


def authentication_ok(rcv, sock):
    pass


def authentication_kerberos_v5(rcv, sock):
    pass


def authentication_cleartext_password(rcv, sock):
    pass


def authentication_md5_password(rcv, sock):
    pass


def authentication_gss(rcv, sock):
    pass


def authentication_sspi(rcv, sock):
    pass


def authentication_sasl(rcv, sock):
    pass


def negotiate_protocol_version(rcv, sock):
    pass
