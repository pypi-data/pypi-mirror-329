import traceback

import requests, json, time, base64
import threading
from retrying import retry


# 定义重试条件
def retry_if_not_expected_code(response, expected_code):
    """如果响应码不是期望的响应码，则重试"""
    return response.status_code != expected_code


class ApiClient:
    def __init__(self, base_url, user_name, password, _print=print):
        self.user_name = user_name
        self.password = password
        self.base_url = base_url
        # 初始化当前令牌和刷新时间
        self.token = None
        self.token_refresh_time = 0
        self.print = _print

        if not self.base_url.startswith('http'):
            raise Exception('请检查base_url格式是否正确')
        if not self.user_name or not self.password:
            raise Exception('请配置正确的用户名和密码')
        # 创建的时候获取令牌
        self.get_access_token()
        # 创建定时器,每一分钟检测一次
        self.token_thread = threading.Thread(target=self.token_thread_func)
        self.token_thread_running = True
        self.token_thread.start()

    def token_thread_func(self):
        while self.token_thread_running:
            self.get_access_token()
            time.sleep(30)

    def get_access_token(self):
        if not self.token or int(time.time()) > self.token_refresh_time:
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{self.user_name}:{self.password}".encode('utf-8')).decode()
            }
            token_result = self.post('/oauth2/token?grant_type=client_credentials', headers=headers)
            self.token = token_result.get('accessToken')
            # 减一分钟，防止网络延迟
            self.token_refresh_time = int(time.time()) + token_result.get('expiresIn') - 60

    @staticmethod
    def handle_response(response):
        response_text = response.text
        if response_text.startswith('{'):
            if response.status_code == 200 and response.json().get('code') == 200:
                return response.json().get('data')
        raise Exception('请求异常:', response.text)

    # 定义重试装饰器,最多30分钟还是失败就报错
    @retry(
        retry_on_result=lambda response: retry_if_not_expected_code(response, 200),  # 重试条件
        stop_max_attempt_number=180,  # 最大重试次数
        wait_fixed=10000,  # 每次重试间隔 30 秒
    )
    def retry_request(self,func):
        try:
            return func()
        except Exception as ex:
            self.print(traceback.format_exc())
            raise Exception('请求异常:', ex)

    def get(self, request_path, request_body=None):
        if request_body is None:
            request_body = {}
        response = self.retry_request(lambda: requests.request("GET", url=f"{self.base_url}/api/v1{request_path}",
                                                               headers={
                                                                   'Authorization': 'Bearer ' + self.token
                                                               },
                                                               params=request_body))
        return self.handle_response(response)

    def post(self, request_path, request_body=None, headers=None):
        if request_body is None:
            request_body = {}
        send_headers = {
        }
        if headers:
            send_headers.update(headers)
        else:
            send_headers.update({'Authorization': 'Bearer ' + self.token})

        response = self.retry_request(lambda: requests.request("POST", url=f"{self.base_url}/api/v1{request_path}",
                                                               headers=send_headers, data=request_body))
        return self.handle_response(response)

    def post_json(self, request_path, request_body=None, headers=None):
        if request_body is None:
            request_body = {}
        send_headers = {
        }
        if headers:
            send_headers.update(headers)
        else:
            send_headers.update({'Authorization': 'Bearer ' + self.token})
        response = self.retry_request(lambda: requests.post(url=f"{self.base_url}/api/v1{request_path}", headers=send_headers, json=request_body))
        return self.handle_response(response)

    def close(self):
        self.token_thread_running = False
        self.token_thread.join()
