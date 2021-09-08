"""
    @File: time_format_handler.py
    @Description: 时间处理模块
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/04/07
"""
from datetime import datetime
import time


def get_time_stamp(mode="history", delta="1d"):
    """
    :return: 当前时间分钟的时间戳作为开始时间，加一天作为结束时间 的列表：[start_time, end_time]
    """
    # 获取当前时分秒
    now = datetime.now()
    time_list = []
    # print(type(now))
    # 获取当前分钟
    now_min = now.strftime('%Y-%m-%d %H:%M:00')
    # print(now_min)
    # 转为时间结构元组
    time_array = time.strptime(now_min, '%Y-%m-%d %H:%M:00')
    # 获取时间戳
    time_stamp = time.mktime(time_array)
    if mode == 'history':
        end_time = round(time_stamp * 1000)   # 去除末尾的小数
        start_time = end_time - 3600 * 24 * 1000
        time_list = [start_time, end_time]
    return time_list


if __name__ == '__main__':
    time_stp = get_time_stamp()
    print(time_stp)
