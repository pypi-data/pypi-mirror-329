# -*- coding: utf-8 -*-
# @Time    : 2024/12/24 13:51
# @Author  : xuwei
# @FileName: log.py
# @Software: PyCharm

import os
import logging
from logging.handlers import RotatingFileHandler


# 在第一次使用的时候才会初始化 logger，self.__init_logger()
class Log:
    def __init__(self):
        """
        3种log handler：1- 输出到文件、输出到控制台、ddp输出到graylog，3个handler可以同时开启
        """
        self.file_handler = True
        self.log_path = './'
        self.name = 'test'  # 决定log文件名称 test.log

        self.console_handler = False

        self.graylog_handler = False
        self.graylog_udp_host = ""
        self.graylog_udp_port = 0

        self.log_level = logging.INFO
        self.log_format = False

        self.__init_log = False

    ## 根据 init_log 修改 self, 只修改一次
    def __init_logger(self):
        if self.__init_log: return
        self.__init_log = True

        self.__logger = logging.getLogger(self.name)
        self.__logger.setLevel(self.log_level)

        formatter = logging.Formatter('[%(levelname)s-%(process)s][%(asctime)s]%(message)s')
        # 确定用哪个handler
        if self.graylog_handler and self.graylog_udp_host:
            import graypy
            graypy_handler = graypy.GELFUDPHandler(self.graylog_udp_host, self.graylog_udp_port)

            graypy_handler.setFormatter(formatter)
            graypy_handler.setLevel(self.log_level)
            self.__logger.addHandler(graypy_handler)

        if self.file_handler:
            log_name = os.path.join(self.log_path, '%s.log' % self.name)
            # file_handler = logging.FileHandler(log_name, 'a', encoding='utf-8')

            # 根据文件大小切割，创建 RotatingFileHandler
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_name,  # 日志文件名
                maxBytes=1024 * 1024 * 5,  # 1024单个日志文件的最大字节数（1KB）, 1024 * 1024 每个文件最大 1MB
                backupCount=5,  # 最多保留 5 个日志文件
                encoding='utf-8'
            )

            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.log_level)
            self.__logger.addHandler(file_handler)

        if self.console_handler:
            # 创建一个StreamHandler,用于输出到控制台
            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)
            console_handler.setLevel(self.log_level)
            self.__logger.addHandler(console_handler)

    def __console(self, level, message):
        self.__init_logger()

        data = message
        if self.name and self.log_format:
            data = {'facility': self.name, 'log_level': level, 'msg': message}
        if level == 'info':
            self.__logger.info(data)
        elif level == 'debug':
            self.__logger.debug(data)
        elif level == 'warning':
            self.__logger.warning(data)
        elif level == 'error':
            self.__logger.error(data)
        elif level == 'except':
            self.__logger.exception(data)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def exception(self, message):
        self.__console('except', message)

    def raise_exception(self, message):
        self.exception(message)
        raise Exception(message)


log = Log()


def init_log(
        file_handler=True,
        log_path='./',
        name='log',

        console_handler=False,

        graylog_handler=False,
        graylog_udp_host: str = "",
        graylog_udp_port: int = 0,

        log_level=logging.INFO,
        log_format=False,
):
    """
    file_path: 存日志文件的文件夹路径
    name: 可以看做是服务的名称，修改name参数，日志文件的前缀名称，默认是 log.error.log，log.info.log
    log_format: 日志输出的格式是否格式化，格式化后是个json [ERROR][2024-01-24 14:04:21,693]{'name': 'test.', 'log_level': 'error', 'msg': 'this is a test2'}
    graylog_udp_host, graylog_udp_port: 为真的话，日志不写文件，而是写入graylog中
    """
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log.file_handler = file_handler
    log.log_path = log_path
    log.name = name

    log.console_handler = console_handler

    log.graylog_handler = graylog_handler
    log.graylog_udp_host = graylog_udp_host
    log.graylog_udp_port = graylog_udp_port

    log.log_level = log_level
    log.log_format = log_format
