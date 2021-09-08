import pytest
import requests

from common.yaml_handler import config_data, security_data


# 登录测试账号
@pytest.fixture()
def login():
    login_host = config_data['login_host']
    url = login_host + 'auth/login'
    method = 'post'
    headers = {'Content-Type': 'application/json'}
    data = {
        "username": security_data['username'],  # username
        "password": security_data['password'],  # password
        "projectName": config_data['project_name'],
        "from": "changshift"
    }

    try:
        resp = requests.request(url=url,
                                method=method,
                                headers=headers,
                                json=data)
    except Exception as e:
        print(e)
        raise e

    res_body = resp.json()
    # print(res_body)
    try:
        assert res_body['code'] == 200
    except AssertionError as e:
        raise e

    # 返回token
    token = res_body['token']
    # print(token)
    # yield token
    return token


if __name__ == '__main__':
    print(123)
    login_token = login()
    print(login_token)
