# coding: utf-8

import functools


# 这个函数是一个装饰器，作用于类对象实例中的每一个方法
# 因为我们修改了class的new方法，并在返回实例后对实例中的函数进行了修改
# ----------------------------
# 如何将修改仅仅作用于对象方法，而不作用于类方法或者类静态方法
#
def inject(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('func:{}, args:{}, kwargs:{}'.format(wrapper.__name__, args, kwargs))
        return func(*args, **kwargs)

    return wrapper

def inject_with_arg(host, port):
    def inj(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('host, port'.format(host, port))
            return func(*args, **kwargs)
        return wrapper

    return inj

# @adecorator
# afunction
# <=> afunction = adecorator(afunction)
# so
# @adecorator_with_arg(arg)
# afunction
# <=> afunction = adecorator_with_arg(arg)(afunction)
# 所以adecorator_with_arg(arg) 需要返回一个装饰器
# 当返回装饰器时使用方法就与无参数时的用法一致，但是通过闭包的原理，我们已经将参数传递给了装饰器
#
@inject_with_arg(host='1.1.1.1', port=11)
def t_inject():
    print('t_inject')

def new_decorater(new_func):
    def wrapper(*args, **kwargs):
        inst = new_func(*args, **kwargs)
        # import pdb;pdb.set_trace()
        for item in dir(inst):
            if not item.startswith('__') and callable(getattr(inst, item)):
                setattr(inst, item, inject(getattr(inst, item)))
        return inst
    return wrapper

class MyMetaClass(type):
    def __new__(cls, classname, bases, attrs):
        nc = super(MyMetaClass, cls).__new__(cls, classname, bases, attrs)
        # import pdb;pdb.set_trace()
        nc.__new__ = new_decorater(nc.__new__)

        return nc

__metaclass__ = MyMetaClass

class A(object, metaclass=MyMetaClass):

    @staticmethod
    def sfunc():
        print('sfunc')

    @classmethod
    def cfunc(cls):
        print('cfunc')

    def __new__(cls, *args, **kwargs):
        print('A,s new function')

        return super(A, cls).__new__(cls)
    a=1
    b=2

    def testf(self):
        pass

k = A()
t = A()
k.testf()
t.testf()

import pdb;pdb.set_trace()
# print(globals())

class Noob(object):
    def __init__(self):
        self.a =1

    def func1(self):
        pass

    def func2(self):
        pass


