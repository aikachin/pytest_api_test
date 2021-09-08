import requests

from middleware.mid_handler import MidHandler


def atest_demo1():
    login_host = MidHandler.config_data['login_host']
    login_api = 'auth/login'
    login_url = login_host + login_api
    method = 'post'
    headers = {'Content-Type': 'application/json'}

    data = {
        "password": MidHandler.security_data['password'],
        "projectName": "minyong",
        "username": MidHandler.security_data['username'],
        "from": "changshift"
    }

    resp = requests.request(url=login_url,
                            method=method,
                            headers=headers,
                            json=data)

    res_body = resp.json()
    print(type(res_body))
    print(res_body)


if __name__ == '__main__':
    atest_demo1()
