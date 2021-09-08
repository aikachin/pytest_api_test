"""
    @File: test_mid_gis.py
    @Description: 描述
    @Author: wangk
    @UPDATED BY: wangk
    @UPDATED: 2021/03/22
"""
import json

import pytest
import allure
import requests

from middleware.mid_handler import MidHandler

data = MidHandler.excel.read('中间层-国惠演示')
civil_host = MidHandler.config_data['civil_host']
my_logger = MidHandler.logger


def format_metric(metric: str):
    """
    :param metric: 中间层接口请求参数中的metric
    :return: metric中各字段的列表
    """
    # me_list = []
    me_list = metric.strip().split(',')
    metric_list_clean = []
    for m in me_list:
        m_list = m.split()
        metric_list_clean.append(m_list[-1])

    return metric_list_clean


@allure.feature("民用演示-国惠")
@allure.story("GIS中间层接口")
@pytest.mark.mid_gis
@pytest.mark.parametrize('test_data', data)
def test_mid_gis(test_data, login):
    """
    中间层接口--GIS
    :param test_data: 测试用例数据
    :param login: 夹具
    :return:
    """
    login_token = login
    MidHandler.logger.info(f'------第{test_data["code"]}条测试用例：{test_data["module"]} - {test_data["case_name"]} 开始执行------')
    # my_logger.info(f'token is:{login_token}') # 默认不打印token到日志中
    MidHandler.logger.info('登录成功！')

    req_url = civil_host + test_data['url']
    req_method = test_data['method']
    req_headers = test_data['headers']
    req_data = test_data['json']

    if test_data['url_param']:
        req_url = ''.join([req_url, test_data['url_param']])

    # 替换 token
    if "#TOKEN" in req_headers:
        req_headers = req_headers.replace("#TOKEN", login_token)

    # 替换时间 startTime(#startTime-min-stp)，endTime(#startTime+1d)
    start_time_flag = 0
    end_time_flag = 0
    # if test_data['code'] == 8:
    #     print('空？？...')

    if "#startTime-min-stp" in req_data:
        start_time = MidHandler.time_stamp_list[0]
        req_data = req_data.replace('#startTime-min-stp', str(start_time))
        start_time_flag = 1

    if "#startTime+1d" in req_data:
        end_time = MidHandler.time_stamp_list[1]
        req_data = req_data.replace('#startTime+1d', str(end_time))
        end_time_flag = 1

    req_data_json = json.loads(req_data)    # 转化为json
    # 时间参数类型还原
    if start_time_flag > 0:
        req_data_json['startTime'] = start_time
    if end_time_flag > 0:
        req_data_json['endTime'] = end_time

    # print('\nreq_data_json', req_data_json)

    resp = requests.request(url=req_url,
                            method=req_method,
                            headers=json.loads(req_headers),
                            json=req_data_json)

    resp_body = resp.json()
    assert resp_body['code'] == 200     # 断言接口是否返回200

    resp_body_data_str = str(resp_body['data'])
    # print('打印响应体数据', resp_body_data_str)    # 打印响应体数据
    expected = json.loads(test_data['expected'])

    # 抽样获取中间层返回接口中的各类型部件数据
    demo_data_dict = {}

    try:
        assert resp_body['data'] != []

        # 校验接口返回数据准确性
        if expected['mode'] == 'GIS initial':
            # expected['p']大致格式为:['部件1': '有', '部件2': '有', '部件3': '无' ...]
            p_list = expected['p']

            # 定义请求体参数中各部件类型查询的属性数据字典，即GIS初始化时，中间层接口查询了哪些种类部件的哪些属性数据
            # 默认为4个：heatboilerroom， heatplant， substation， measuredpoint
            request_p_data_dict = {}
            for request_p in req_data_json['queries']:
                request_p_data_dict[request_p['table']] = request_p['metric']

            # 校验查询的部件是否有数据
            for p in p_list:
                if p[1] == '无':
                    assert p[0] not in resp_body_data_str  # 在返回数据中无此类型部件数据
                elif p[1] == '有':
                    assert p[0] in resp_body_data_str  # 在返回数据中有此类型部件数据

                    # 获取返回部件数据的详细字段，为确保校验返回数据字段和请求的字段没有遗漏做准备
                    for d in resp_body['data']:
                        if p[0] in str(d):
                            # print('有此类型部件')
                            demo_data_dict[p[0]] = d
                            # 只要获取到一条匹配类型部件的数据就退出本轮循环。
                            # 这块暂时没有好的优化方法，先这么做着
                            break
                else:
                    my_logger.error(f'测试用例数据有误!请检查expected数据：{expected}')

            # 验证GIS初始化查询中各部件的结果数据中各字段是否都有返回
            for k_act, v_act in demo_data_dict.items():  # 此处的 _act 表示实际接口返回的数据
                # 获取metric的列表形式
                metric_list = format_metric(request_p_data_dict[k_act])
                for metric in metric_list:
                    # 验证各个查询字段在返回结果中都有出现
                    try:
                        assert metric in v_act
                    except AssertionError as e:
                        my_logger.error(f'{metric}没有出现在{k_act}的结果数据中！问题数据为：{v_act}')
                        print(e)
        else:
            # 定义请求体参数中各部件类型查询的属性数据字典
            request_p_data_dict = req_data_json['queries'][0]
            # 获取metric的列表形式
            metric_list = format_metric(request_p_data_dict['metric'])
            # 获取中间层返回接口中的部件数据
            # print("resp_body['data']:", resp_body['data'])
            # print("resp_body['data']大小:", len(resp_body['data']))
            demo_data_dict = resp_body['data'][0]
            # 部件数据类型
            p_type = req_data_json['table']
            for metric in metric_list:
                assert metric in demo_data_dict
            # 断言接口数据中有aligntime
            assert 'aligntime' in demo_data_dict
            # 断言接口数据类型
            assert p_type == demo_data_dict['type']

            # 断言pid是否一致
            if req_data_json['search']:
                assert req_data_json['search'].split('pid=')[1] == str(demo_data_dict['pid'])

    except Exception as e:

        if 'mode' in expected.keys():
            if '' == req_data_json['table']:
                my_logger.error('测试用例数据有误!请检查测试用例的json列数据的"table"！')
            else:
                my_logger.warning(f"{req_data_json['table']} 没有数据！")

            # if expected['mode'] == 'history':
            #     my_logger.warning(f"{expected['type']} 24小时历史数据为空！")
            # elif expected['mode'] == 'real':
            #     my_logger.warning(f"{expected['type']} 没有工况数据！")
            # elif expected['mode'] == 'calc':
            #     my_logger.warning(f"{expected['type']} 没有计算数据！")
            # else:
            #     my_logger.error("没有任何工况数据！请检查数据对接！")
        else:
            my_logger.error(f'测试用例数据有误!请检查expected数据：{expected}')

    my_logger.info(f'------第{test_data["code"]}条测试用例：{test_data["module"]} - {test_data["case_name"]} 执行结束------')


# if __name__ == '__main__':
#     test_mid_gis()

