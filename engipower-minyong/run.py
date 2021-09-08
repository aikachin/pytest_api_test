"""
    @File: run.py
    @Description: 描述
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/04/07
"""
import os

import pytest

from middleware.mid_handler import MidHandler

if __name__ == '__main__':
    MidHandler.logger.info('------------测试开始------------')

    report_path = ''.join([MidHandler.report_file, '_', MidHandler.time_fmt, '.html'])
    """
    参数说明：
    -v: 显示用例执行中间过程
    -m: 标记（marker）用于标记测试脚本并分组，以便快速选中并运行
    -s: 显示程序中的print/logging输出；禁用测试报告中的打印输出（只有在用例失败时才显示）
    """
    pytest.main(['-v', '-m mid_measurepoint', f'--html={report_path}'])

    MidHandler.logger.info('------------测试结束------------\n')

    # report_path = ''.join([MidHandler.report_file, '_', MidHandler.time_fmt])
    # pytest.main(['-v', '-m mid_gis'])
    # pytest.main(['-v', '-m mid_gis', f'--alluredir={report_path}'])
