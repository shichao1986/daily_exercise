# -*- coding: utf-8 -*-
"""
时间: 2019/8/29 11:17

作者: shichao

更改记录:

重要说明:
"""

import os
import sys
from cfg import a


a += 1

print('a={}'.format(a))

while True:

    cc = input('sss')
    c = int(cc)
    if c == 0:
        # import pdb;pdb.set_trace()
        try:
            # windows 无法执行, ubuntu 验证后 a每次的输出为11，说明进程的内存空间被重置了
            os.execl(sys.executable, os.path.split(sys.executable)[1], *sys.argv)
        except Exception as e:
            print('{}'.format(e))

