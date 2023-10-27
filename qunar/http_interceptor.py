import aiohttp
import json
import copy
import time

"""
http拦截器,用于拦截openai的请求,并将请求转发到qunar的接口
"""

qunar_data_t = {
    "key": "yangx.xiao",
    "password": "123456",
    "apiType": "gpt-35-turbo"
}

original_request = None


# 定义新的_request方法
async def new_request(self, method, url, **kwargs):
    print(f"Intercepted request: {method} {url}")
    tmstmp = int(time.time())
    if method == "post" and url == "https://api.openai.com/v1/chat/completions":
        data_s = kwargs.get('data')
        data = json.loads(data_s)
        qunar_data = copy.copy(qunar_data_t)
        qunar_data['prompt']['message'] = data['message']
        qunar_data_s = json.dumps(qunar_data)
        url = "qunar.com"
        kwargs['data'] = qunar_data_s

    response = await original_request(self, method, url, **kwargs)

    if str(response.url) == "https://api.openai.com/v1/chat/completions" and response.status == 200:

        data = await response.json()

        if data['status'] == 1:
            response.status = 400
            return response

        data = await response.json()
        choices = build_choices(data)
        new_data = {"id": tmstmp, "object": "chat.completion.chunk", "created": tmstmp, "model": "gpt-3.5-turbo",
                    "choices": choices}
        response._body = json.dumps(new_data).encode()

    return response


def build_choices(qunar_d):
    status = qunar_d['data']['current_status']
    data = qunar_d['data']['currentText']

    choice = {}

    delta = {}
    finish_reason = None

    if status == 'begin':
        delta['role'] = 'assistant'
        delta['content'] = ''
    elif status == 'executing':
        delta['content'] = data
    else:
        finish_reason = 'stop'

    choice['delta'] = delta
    choice['index'] = 0
    choice['finish_reason'] = finish_reason
    return [choice]


def init():
    global original_request
    original_request = aiohttp.ClientSession._request
    aiohttp.ClientSession._request = new_request
