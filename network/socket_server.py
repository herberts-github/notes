# -*- coding:utf-8 -*-
# 简单 Web Server
# 通过 socket 实现 Web 服务
# 通过监听本地 8000 端口，接收客户端发来的数据，然后返回对应 HTTP 响应
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1>PYTHON</h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sun, 27, six, 2021 00:00:00 GMT',
    # 'Content-Type: text/plain; charset=utf-8',
    'Content-Type: text/html; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    # 当我们处于单进程、单线程模型时，程序接受一个请求，然后花 100s 处理
    # 此时新的请求是进不来的，因为只有一个处理程序
    # print('oh, new conn', conn, addr)
    # import time
    # time.sleep(100)

    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    conn.send(response.encode())  # response 转为 bytes 后传输
    conn.close()


def main():
    # socket.AF_INET 用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM 用于基于 TCP 流式 socket 通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证每次 Ctrl+C 组合键之后，快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', 8000))
    serversocket.listen(5)  # 设置 backlog-socket 连接最大排队数量
    print('http://localhost:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connection(conn, address)
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
