"""
    @File: mid_handler.py
    @Description: 描述
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/03/26
"""
import os
from datetime import datetime

from common.excel_handler import ExcelHandler
from common.logging_handler import get_logger
from common.time_format_handler import get_time_stamp
from common.yaml_handler import read_yaml
from config import path


class MidHandler:
    # 时间格式化yyyy-mm-dd HH:MM:ss
    time_fmt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 基础配置
    config_path = path.config_path
    config_data = read_yaml(config_path)
    # 测试用例数据
    excel_path = os.path.join(path.excel_dir, config_data['case_file'])
    # 账号信息
    security_path = path.security_path
    security_data = read_yaml(security_path)
    # 报告路径
    report_path = path.report_dir
    report_file = os.path.join(report_path, config_data['report_file'])

    # 获取时间戳
    time_stamp_list = get_time_stamp()

    # excel handler
    excel = ExcelHandler(excel_path)

    # 日志处理模块
    log_path = os.path.join(path.log_dir, config_data['log_file'])
    logger = get_logger(name=config_data['log_name'],
                        file_name=log_path)

    # logger.info('excel_path:', excel_path)


if __name__ == '__main__':
    pass
