"""
    @File: yaml_handler.py
    @Description: yaml处理模块
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/04/07
"""
import yaml
from config import path


# 读取yaml文件内容
def read_yaml(file):
    with open(file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data


# 基础配置
config_path = path.config_path
config_data = read_yaml(config_path)
# 账号信息
security_path = path.security_path
security_data = read_yaml(security_path)

