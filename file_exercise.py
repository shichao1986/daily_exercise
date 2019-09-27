# -*- coding: utf-8 -*-
"""
时间: 2019/6/4 15:57

作者: shichao

更改记录:

重要说明:
"""

def create_big_file(name):
    try:
        with open(name, 'w') as f:
            f.write('123')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_big_file('bigfile')

