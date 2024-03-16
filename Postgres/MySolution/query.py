from table import Table

table_recieved = False


def handler(conn, rcv: [bytes]):
    table = Table(conn, 'query response')
    for i in rcv:
        func = HANDLER.get(i.decode('utf-8', errors='ignore')[0])
        if func is data_row or func is row_description:
            func(i, table)
    if tablse_recieved:
        return table
    return False


def command_complete(cmd):
    completed = cmd[5:].decode('utf-8', errors='ignore')
    print(f'Command: {completed}')


def copy_in_response(cmd):
    pass


def copy_out_response(cmd):
    pass


def row_description(cmd, table):

    table_recieved = True


def data_row(cmd, table):
    return True


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


HANDLER = {'C': command_complete,
           'G': copy_in_response,
           'H': copy_out_response,
           'T': row_description,
           'D': data_row,
           'I': empty_query_response,
           'E': error_response,
           'Z': ready_for_query,
           'N': notice_response
           }