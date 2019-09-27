# -*- coding: utf-8 -*-
"""
时间: 2019/9/5 11:39

作者: shichao

更改记录:

重要说明:
"""
from socketserver import BaseRequestHandler,ThreadingTCPServer
import time
import threading

fields = ['1',2,'3']

def period_send(fd, interval):
    it = max(interval, 3)

    try:
        while True:
            print('send message...')
            #fd.sendall(('{},{},{}'.format(fields[0], '\x02', fields[2])).encode('utf-8'))
            # fd.sendall(b'\x76,\x77,\x68')
            fd.sendall(b'\x76,\x77,\x78')
            fields[0] = str(int(fields[0]) + 1)
            fields[2] = str(int(fields[2]) + 3)
            time.sleep(it)
    except Exception as e:
        print(e)
        fd.close()

class Handler(BaseRequestHandler):
    BUF_SIZE = 4096
    def __init__(self, request, client_address, server):
        super(Handler, self).__init__(request, client_address, server)

    def handle(self):
        self.ip_addr,self.port = self.client_address

        threading.Thread(target=period_send, args=(self.request, 3)).start()

        while True:
            try:
                data = self.request.recv(Handler.BUF_SIZE)

                if len(data) <= 0:
                    print('client[{}] disconnect this socket!'.format(self.client_address))
                    break

                print('data:{}'.format(data))

            except Exception as e:
                print(e)
                break

def start_server(addr):
    server = ThreadingTCPServer(addr, Handler,bind_and_activate = False)  # 参数为监听地址和已建立连接的处理类
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server.serve_forever()  # 监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理

if __name__ == '__main__':
    start_server(('0.0.0.0', 8765))