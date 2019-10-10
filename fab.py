# -*- coding: utf-8 -*-
"""
时间: 2019/7/18 10:19

作者: shichao

更改记录:

重要说明:
"""
import random
import logging
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

    LOGGER = logging.getLogger()


    try:
        try:
            # raise MyException()
            pass
        # except MyException as e:
        #     print(e)
        # except Exception as e:
        #     import pdb;pdb.set_trace()
        #     print(type(e))
        finally:
            print(1)
    except Exception as e:
        print(2)
