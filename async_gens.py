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
        print(tasks)
        while not tasks:
            print('Check sockets')
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
    try:
        task = tasks.pop(0)
        print('Task:', task.__name__)
        action, sock = task.__next__()

        if action == 'read':
            to_read[sock] = task

        if action == 'write':
            to_write[sock] = task
    except StopIteration:
        print('Done!')


tasks.append(server())

event_loop()


