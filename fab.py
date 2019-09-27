# -*- coding: utf-8 -*-
"""
时间: 2019/7/18 10:19

作者: shichao

更改记录:

重要说明:
"""

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

if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    while True:
        n = input('please input number:')
        n = int(n)
        print('fab({}) list is:{}'.format(n, [fab(i) for i in range(1, n + 1)]))
        for k in fab_iter(n):
            print(k)
        # print('fab_iter({})={}'.format(n, [i for i in fab_iter(n + 1)]))
