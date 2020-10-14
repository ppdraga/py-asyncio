

import socket
import sys

URLS = {
    '/': 'HELLO INDEX',
    '/blog': 'HELLO BLOG'
}


def generate_header(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 Method not alowed\n\n', 405
    if not url in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200

def generate_body(code, url):
    if code == '404':
        return '<h1>404</h1><p>Not found</p>'
    if code == '405':
        return '<h1>405</h1><p>Method not alowed</p>'
    try:
        return URLS[url]
    except Exception as e:
        return str(sys.exc_info())

def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_header(method, url)
    body = generate_body(code, url)
    return (headers + body).encode()

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request.decode('utf-8'))
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
