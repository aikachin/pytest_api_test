"""
    @File: logging_handler.py
    @Description: 日志处理模块
    @Author: wangk
    @UPDATED BY: wangk
@   UPDATED: 2021/03/22
"""
import logging
import os

from config.path import log_dir


def get_logger(name='Engipower',
               logger_level='DEBUG',
               file_name=None,
               stream_handler_level='DEBUG',
               file_handler_level='DEBUG',
               # %(funcName)s 记录当前方法名
               fmt='%(asctime)s %(name)s [%(filename)s] [%(levelname)s] [line:%(lineno)d] %(message)s'):
    logger = logging.getLogger(name)  # 获取收集器
    logger.setLevel(logger_level)     # 定义日志输出等级

    handler = logging.StreamHandler()   # 定义日志处理器
    handler.setLevel(stream_handler_level)

    # 定义日志输出格式
    handler_fmt = logging.Formatter(fmt)
    handler.setFormatter(handler_fmt)

    file_handler = logging.FileHandler(file_name, 'a', 'utf-8')    # 定义日志文件处理器
    file_handler.setLevel(file_handler_level)
    file_handler.setFormatter(handler_fmt)

    logger.addHandler(handler)  # 收集器添加处理器
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    log_path = os.path.join(log_dir, 'myLog.log')
    my_logger = get_logger(file_name=log_path)
    my_logger.log(10, '123')
