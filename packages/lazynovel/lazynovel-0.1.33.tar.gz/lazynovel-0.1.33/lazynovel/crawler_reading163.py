#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
import requests
import json


def login(
        username: str,
        password: str
):
    """
    使用账号密码登录系统
    :param username: 账号
    :param password: 密码
    :return:
    登录成功返回：{'code': 200, 'data': {'isFinance': 0}}
    登录失败返回：{'code': 500, 'message': '密码校验失败'}
    """
    url = 'https://bi.reading.163.com/login'
    method = 'POST'
    json_data = {
        'userName': username,
        'password': password
    }
    response = requests.request(
        method=method,
        url=url,
        json=json_data
    )
    return {'response': response.json(), 'cookie': response.headers.get('Set-Cookie')}


def get_apps(
        cookie: str,
        page: int = 1
):
    """
    获取子账号信息
    :param cookie: cookie字符串
    :param page: 页码
    :return:
    """
    url = 'https://bi.reading.163.com/open/query'
    method = 'GET'
    params = {
        'page': page
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "bi.reading.163.com",
        "Referer": "https://bi.reading.163.com/spa/open",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    return lazyrequests.lazy_requests(
        method=method,
        url=url,
        params=params,
        headers=headers,
        return_json=True
    )


def customer_message_add_or_update(
        content: str,
        send_time: int,
        send_type: int,
        site_id: int,
        title: str,
        msg_type: int,
        cookie: str,
        recharge_type: int = None
):
    """
    小说管理-公众号运营-添加客服消息
    :param content: 消息内容
    :param send_time: 发送时间（13位时间戳）
    :param send_type: 触达人群，0｜全部用户，1｜按标签选择
    :param site_id: 公众号id
    :param title: 消息名称
    :param msg_type: 消息类型，图文消息：0，文字消息：4，图片消息：2
    :param cookie: cookie
    :param recharge_type: 按标签选择-充值类型，0｜未充值,1｜已充值
    :return: {"code":200}
    """
    url = 'https://bi.reading.163.com/customer/message/addOrUpdate'
    method = 'POST'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Host": "bi.reading.163.com",
        "Origin": "https://bi.reading.163.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    json_data = {
        "title": title,  # 消息名称
        "sendTime": send_time,  # 发送时间（13位时间戳）
        "content": content,  # 消息内容
        "type": msg_type,  # 消息类型，图文消息：0，文字消息：4，图片消息：2
        "siteId": site_id,  # 公众号id
        "sendType": send_type  # 触达人群，全部用户：0，按标签选择：1
    }
    if recharge_type is not None:
        json_data['tagInfo'] = json.dumps(
            {
                'rechargeType': recharge_type,
                'siteId': site_id
            }
        )
    # print('json_data:', json_data)
    response = requests.request(
        method=method,
        url=url,
        json=json_data,
        headers=headers
    )
    if response.status_code == 200:
        return {
            'status_code': response.status_code,
            'response': response.json()
        }
    else:
        return {
            'status_code': response.status_code,
            'response': {}
        }  # 需要登录


def antispam_text(
        content: str,
        cookie: str
):
    """
    发送客服消息时的文本校验
    :param content:
    :param cookie:
    :return:
    成功返回：
    {
        "code": 200,
        "message": "success"
    }
    """
    url = 'https://bi.reading.163.com/antispam/text'
    method = 'POST'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Host": "bi.reading.163.com",
        "Origin": "https://bi.reading.163.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    json_data = {
        'antispamType': 1,
        'content': content
    }
    response = requests.request(
        method=method,
        url=url,
        json=json_data,
        headers=headers
    )
    if response.status_code == 200:
        return {
            'status_code': response.status_code,
            'response': response.json()
        }
    else:
        return {
            'status_code': response.status_code,
            'response': {}
        }  # 需要登录
