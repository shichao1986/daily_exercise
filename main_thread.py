# -*- coding: utf-8 -*-
"""
时间: 2019/10/25 10:54

作者: shichao

更改记录:

重要说明:
"""

import threading

import logging
import time

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
fmt = '%(name)s %(levelname)s %(filename)s %(funcName)s %(message)s'
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(fmt))
LOGGER.addHandler(ch)

def loop():
    while True:
        print('do one task!')
        time.sleep(1)

class task(object):

    @classmethod
    def start(cls):
        threading.Thread(target=loop, daemon=True).start()

# class newtask(threading.Thread):
#     def __init__(self):
#         super(newtask, self).__init__()
#         self.start()
#
#     def run(self):
#         while True:
#             print('do newtask once!')
#             time.sleep(1)

# class thridtask(threading.Thread):
#     @classmethod
#     def start(self):
#         threading.Thread(target=loop).start()

if __name__ == '__main__':
    # class类静态方法创建的线程无法像预期一样执行
    task.start()

    # threading.Thread(target=loop, daemon=True).start()

    # nt = newtask()

    # thridtask.start()

    # gc.collect()