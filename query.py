

HANDLER = {'C': lambda cmd: command_complete(cmd),
           'G': lambda cmd: copy_in_response(cmd),
           'H': lambda cmd: copy_out_response(cmd),
           'T': lambda cmd: row_description(cmd),
           'D': lambda cmd: data_row(cmd),
           'I': lambda cmd: empty_query_response(cmd),
           'E': lambda cmd: error_response(cmd),
           'Z': lambda cmd: ready_for_query(cmd),
           'N': lambda cmd: notice_response(cmd)
           }


def handler(rcv: [bytes]):
    for i in rcv:
        func = HANDLER.get(i.decode('utf-8', errors='ignore')[0])
        func(i)


def command_complete(cmd):
    completed = cmd[5:].decode('utf-8', errors='ignore')
    print(f'Command: {completed}')


def copy_in_response(cmd):
    pass


def copy_out_response(cmd):
    pass


def row_description(cmd):
    pass


def data_row(cmd):
    pass


def empty_query_response(cmd):
    print('Empty Query')


# Later add parse error message
def error_response(cmd):
    err_msg = cmd[5:].decode('utf-8', errors='ignore')
    print(f'Error: {err_msg}')


def ready_for_query(cmd):
    transaction_status = {'I': 'Not in a transaction block',
                          'T': 'In a transaction block',
                          'E': 'In a failed transaction block (queries will be rejected until block is ended)'
                          }
    s = transaction_status.get(cmd.decode('utf-8', errors='ignore')[-1])
    print('Ready for query: ', s)


# Later add field parser
def notice_response(cmd):
    print(cmd[5:].decode('utf-8', errors='ignore'))
