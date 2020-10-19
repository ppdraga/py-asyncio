# David Beazley

import socket
from select import select


tasks = []

# Conection between sockets and generators!
# Two dicts to split sockets by read/write, it needs for select (which will listen all the sockets)

to_read = {}        # {socket: generator, socket2: generator2, ...}
to_write = {}       # {socket: generator, socket2: generator2, ...}

def server():
    print('Server socket init start')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    print('Server socket init end')

    while True:
        print('Server yield')
        yield ('read', server_socket)    # add server_socket to read for select
        print('Before .accept() waiting for connections')
        client_socket, addr = server_socket.accept()    # read
        print('Connection from ', addr)
        print('Init new client generator and add it to tasks for socket', addr)
        tasks.append(client(client_socket))



def client(client_socket):
    while True:
        try:
            sockname = client_socket.getpeername()
        except OSError:
            sockname = client_socket.getsockname()
        print('Client yield read', sockname)

        yield ('read', client_socket)    # add client_socket to read for select
        print('Reading data')
        request = client_socket.recv(1024)  # read

        if not request:
            break
        else:
            response = 'Hello world\n'.encode()
            print('Client yield write ', client_socket.getpeername())
            yield ('write', client_socket)    # add client_socket to write for select
            print('Sending data')
            client_socket.send(response)    # write

    print('Outside inner while loop - client_socket.close()')
    client_socket.close()




def event_loop():
    print('Main event loop!')
    while any([tasks, to_read, to_write]):
        # Debug info
        to_read_str = ['{}-{}'.format(t[0].getsockname() if t[1].__name__ == 'server' else t[0].getpeername(), t[1].__name__) 
            for t in to_read.items()] if to_read else 'empty'
        to_write_str = ['{}-{}'.format(t[0].getpeername(), t[1].__name__) for t in to_write.items()] if to_write else 'empty'
        print('tasks:', [t.__name__ for t in tasks], 
            '\nto_read:', to_read_str, 
            '\nto_write:', to_write_str)

        while not tasks:
            print('Check sockets\n')
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            print('Spread sockets to tasks')

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

                try:
                    sockname = sock.getpeername()
                except OSError:
                    sockname = sock.getsockname()
                print('Socket', sockname, 'put generator to tasks (from to_read)')

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
                print('Socket', sock.getpeername(), 'put generator to tasks (from to_write)')

        try:
            task = tasks.pop(0)
            print('Task execution:', task.__name__)
            action, sock = task.__next__()

            try:
                sockname = sock.getpeername()
            except OSError:
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


