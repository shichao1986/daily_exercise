# -*- coding: utf-8 -*-
"""
时间: 2019/7/18 10:19

作者: shichao

更改记录:

重要说明:
"""
import random
import logging
import sys
import threading
import time
def fab(n):
    if not isinstance(n, int):
        raise TypeError('n is not a Integer!')

    if n < 1:
        raise Exception('n is a invalid value:{}!'.format(n))
    elif n < 3:
        return 1
    else:
        a = 1
        b = 1
        for i in range(2, n):
            ret = a + b
            a, b = b, a+b
        return ret

def fab_iter(n):
    if not isinstance(n, int):
        return
    a = 1
    b = 1
    for i in range(1, n + 1):
        if i < 3:
            yield 1
            continue
        ret = a + b
        yield ret
        a, b = b, a+b
    return

class A(object):
    def __init__(self, n=5):
        self.a = 1
        self.b = 1
        self.n = n

    def __next__(self):
        if self.index >= self.n:
            raise StopIteration
        else:
            self.index += 1
            if self.index > 2:
                ret = self.a + self.b
                self.a, self.b = self.b, self.a + self.b
                return ret
            else:
                return 1


    def __iter__(self):
        self.index = 0
        return self

class B(object):
    def __init__(self, n=5):
        self.a = 1
        self.b = 1
        self.n = n
        self.index = 0
    def __iter__(self):
        self.index = 0
        while self.index < self.n:
            if self.index < 2:
                yield 1
            else:
                yield self.a + self.b
                self.a, self.b = self.b, self.a + self.b
            self.index += 1


        # yield 1
        # yield 2
        # yield 3

class MyException(Exception):
    def __str__(self):
        return 'my exception'

def func():
    assert False, 'false assertion'
    assert False, 'false2 assertion'

# 函数对象第一次初始化会将每个参数的默认值存储在func2.__defaults__内，这是一个tuple
# 后续函数运行时，对应的变量会取其中的值作为初始参数，对于普通的数据类型，函数内部
# 不易改变函数参数的默认值，但若参数的默认值为可变数据类型，则函数内部很容易修改默认值
# 这在大部分函数应用场景都与预期不符。所以函数默认值一般设置成None，而不使用list或字典
def func2(testlist=[]):
        print('inner func2 input testlist={}'.format(testlist))
        testlist.append(1)
        return testlist
def func3(testlist=None):
    cc = testlist
    print(cc)
    # func3.__defaults__ = ([],)
    return testlist

a = dict()

class ttt(object):
    def __init__(self):
        self._abc = 1

    @property
    def abc(self):
        return self._abc


class mytask(threading.Thread):

    def __init__(self):
        super(mytask, self).__init__()
        self.start()

    def run(self):
        while True:
            print('do task once!')
            time.sleep(1)


if __name__ == '__main__':
    # while True:
    #     n = input('please input number:')
    #     n = int(n)
    #     print('fab({}) list is:{}'.format(n, [fab(i) for i in range(1, n + 1)]))
        # for k in fab_iter(n):
        #     print(k)
        # a = A(10)
        # for k in a:
        #     print(k)

    # b = B(10)
    # for k in b:
    #     print(k)
    #     # print('fab_iter({})={}'.format(n, [i for i in fab_iter(n + 1)]))

    # LOGGER = logging.getLogger()
    # # func()
    #
    # nl = func2()
    # print(nl)
    #
    # nl.append(100)
    #
    # nl2 = func2()
    # print(nl2)
    #
    # func3()

    t = ttt()

    print('abc={}'.format(t.abc))

    nt = mytask()

    # try:
    #     a['123'] = 123
    #     raise MyException('123')
    # except MyException as e:
    #     print(e)
    #     excp = sys.exc_info()[1]
    #     print(excp)


