# -*- coding: utf-8 -*-
"""
时间: 2019/9/29 14:01

作者: shichao

更改记录:

重要说明:
"""

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.netutil
import tornado.process

class helloHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('hello world')


my_app = tornado.web.Application(
    [('/',helloHandler),]
)

if __name__ == '__main__':
    # # 单线程启动app
    # my_app.listen(8888)
    #
    # # 用服务的方式启动
    # # 1 单进程启动，与tornado.web.Application.listen() 相同，httpserver运行在当前进程
    # my_server = tornado.httpserver.HTTPServer(my_app)
    # my_server.listen(8888)
    #
    # # 2 多进程启动，每个进程运行一个httpserver
    # my_server = tornado.httpserver.HTTPServer(my_app)
    # my_server.bind(8888)
    # my_server.start(0)

    # 3 更高级的多进程启动，可以对sockets进行配置
    sockets = tornado.netutil.bind_sockets(8888)
    tornado.process.fork_processes(0)
    server = tornado.httpserver.HTTPServer(my_app)
    server.add_sockets(sockets)







    tornado.ioloop.IOLoop.current().start()