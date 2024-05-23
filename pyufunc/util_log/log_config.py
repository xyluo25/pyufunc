# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, July 12th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo

# some code adopt form https://github.com/ydf0509/nb_log
##############################################################

import logging


LOG_FORMATTER = {
    1: logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    2: logging.Formatter(
        '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s - File "%(pathname)s", line %(lineno)d ', "%Y-%m-%d %H:%M:%S"),  # 这个也支持日志跳转
    3: logging.Formatter(
        '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),
    4: logging.Formatter('%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',
                         "%Y-%m-%d %H:%M:%S"),
    5: logging.Formatter('%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',
                         "%Y-%m-%d %H:%M:%S"),  # 一个只显示简短文件名和所处行数的日志模板
    6: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 对3改进，带进程和线程显示的日志模板。
    7: logging.Formatter(
        '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S"),  # 对5改进，带进程和线程显示的日志模板。
}

FORMATTER_KIND = 3  # 如果get_logger不指定日志模板，则默认选择第几个模板+