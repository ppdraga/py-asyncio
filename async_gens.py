# David Beazley

import socket
from select import select


tasks = []

to_read = {}        # {socket: generator}
to_write = {}       # {socket: generator}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        print('Before .accept() waiting for connections')
        client_socket, addr = server_socket.accept()    # read
        print('Connection from', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        print('Reading data')
        request = client_socket.recv(1024)  # read

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()
            yield ('write', client_socket)
            print('Sending data')
            client_socket.send(response)    # write

    print('Outside inner while loop - client_socket.close()')
    client_socket.close()




def event_loop():
    print('Main event loop!')
    while any([tasks, to_read, to_write]):
        to_read_str = ['{}-{}'.format(t[0].getsockname(), t[1].__name__) for t in to_read.items()] if to_read else 'empty'
        to_write_str = ['{}-{}'.format(t[0].getsockname(), t[1].__name__) for t in to_write.items()] if to_write else 'empty'
        print('tasks:', [t.__name__ for t in tasks], 
            '\nto_read:', to_read_str, 
            '\nto_write:', to_write_str)
        while not tasks:
            print('Check sockets')
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            print('Spread sockets to tasks')

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
                print('Socket', sock.getsockname(), 'added to read')

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
                print('Socket', sock.getsockname(), 'added to write')

        try:
            task = tasks.pop(0)
            print('Task execution:', task.__name__)
            action, sock = task.__next__()

            sockname = sock.getsockname()
            print(f'Returned after execution: action: {action}, socket: {sockname}')
            if action == 'read':
                to_read[sock] = task
                print('Added to dict: to_read[{}]={}'.format(sockname, task.__name__))

            if action == 'write':
                to_write[sock] = task
                print('Added to dict: to_write[{}]={}'.format(sockname, task.__name__))


        except StopIteration:
            print('Done!')


tasks.append(server())

event_loop()


