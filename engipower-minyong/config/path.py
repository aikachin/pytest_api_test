"""
    @File: path.py
    @Description: 文件路径/目录模块
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/04/07
"""
import os


# 当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
# 根目录
root_dir = os.path.dirname(current_dir)

# 配置文件目录
config_dir = os.path.join(root_dir, 'config')
# 配置文件路径
config_path = os.path.join(config_dir, 'config.yaml')
# 账号文件路径
security_path = os.path.join(config_dir, 'security.yaml')
# 测试用例 excel 目录
excel_dir = os.path.join(root_dir, 'cases')

# 日志目录
log_dir = os.path.join(root_dir, 'log')
# 报告目录
report_dir = os.path.join(root_dir, 'report')
