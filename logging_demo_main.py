# -*- coding: utf-8 -*-
"""
时间: 2019/10/10 16:43

作者: shichao

更改记录:

重要说明: logging模块说明
所有的打印都是通过Logger执行的，打印级别从低到高为debug,info,warning,error,critical
logging模块提供了默认的root Logger，该Logger具备streamHandler，默认打印级别是warning
如果不配置任何Logger，直接使用logging模块打印，则使用默认的root Logger进行打印
basicConfig方法是对root Logger进行配置，formatter是对handdler进行配置的，一个Logger可以有多个handdler
handler和Logger都可以设置打印级别，Logger在打印内容时，一条消息能否在其内部的handler上打印内容取决于
该条消息的打印级别是否满足：大于等于Logger的打印级别 and 大于等于该streamHandler的打印级别

root Logger是所有其他Logger的默认Logger，当任何一个Logger在打印内容是没有Handler，则会使用root Logger的所有handlers进行打印

除了root Logger 意外的Logger存在父子关系，父子关系通过Logger的名称来确定，父子关系通过'.'来表示，例如
Logger A 是Logger A.B 的父亲 ，Logger A.B 是 Logger A.B.C的父亲
具有亲缘关系的Logger（A、A.B、A.B.C, 父亲-儿子-孙子），晚辈的打印消息会同时传递给其所有长辈Logger，并使用这些长辈各自的
handdler进行打印，当所有长辈和其自身均不存在handler时才会使用root Logger进行打印。

常见模块打印用法：
一般python 模块会在内部定义LOGGER = logging.getLogger(__name__)
（__name__的特性决定了模块之间自动使用.进行连接）
例如：
from A.B.C.D import E
E 为一个模块（E.py），E.py内部的LOGGER = logging.getLogger(__name__) 的名称为A.B.C.D.E

可以在main中初根据实际需要始化Logger的配置，
如果需要对A进行整体打印输出，则只需要getLogger(A),在进行配置即可
如果需要更细致的打印输出，就对各级Logger进行配置，但是要谨记，具有亲缘关系的Logger之间的消息传递规则

That's all !     O(∩_∩)O
"""
import sys
import logging

import logging_demo_a
import logging_demo_b

from logging_demo_files import logging_demo_c

LOGGER_FATHER = logging.getLogger('abc')

LOGGER = logging.getLogger('abc.def')
# LOGGER.setLevel(logging.ERROR)

LOGGER_CHILD = logging.getLogger('abc.def.ghi')
# LOGGER_CHILD.setLevel(logging.ERROR)

# LOGGER_TEST = logging.getLogger('test')
# LOGGER_TEST.setLevel(logging.INFO)

if __name__ == '__main__':
    fmt = '%(name)s %(levelname)s %(filename)s %(funcName)s %(message)s'
    # logging.basicConfig(level=logging.INFO, format=fmt, filename='log.log', filemode='w')
    # logging.basicConfig(level=logging.INFO, format=fmt)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(fmt))
    ch.setLevel(logging.WARNING)
    fh = logging.FileHandler('log.log', mode='w')
    fh.setLevel(logging.ERROR)

    # LOGGER_FATHER.addHandler(fh)
    # LOGGER_FATHER.addHandler(ch)

    # LOGGER.addHandler(fh)
    LOGGER.addHandler(ch)
    # logging.warning('logging message')
    # LOGGER.warning('warning message:{}'.format(__name__))
    # LOGGER_TEST.warning('test info')
    LOGGER_CHILD.error('{} error message:{}'.format(sys._getframe().f_lineno, __name__))
    # logging_demo_a.test_logger_log_a()
    # logging_demo_b.test_logger_log_b()
    # logging_demo_c.test_logger_log_c()