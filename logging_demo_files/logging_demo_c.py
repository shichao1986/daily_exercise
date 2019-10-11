# -*- coding: utf-8 -*-
"""
时间: 2019/10/10 16:43

作者: shichao

更改记录:

重要说明:
"""

import logging

LOGGER = logging.getLogger(__name__)

def test_logger_log_c():
    LOGGER.debug('debug message:{}'.format(__name__))
    LOGGER.info('info message:{}'.format(__name__))
    LOGGER.warning('warning message:{}'.format(__name__))
    LOGGER.error('error message:{}'.format(__name__))
    LOGGER.critical('critical message:{}'.format(__name__))