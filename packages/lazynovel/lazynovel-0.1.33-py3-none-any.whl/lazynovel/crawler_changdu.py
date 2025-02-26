#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
from lazysdk import lazytime


def create_customer_service_message(
        token: str,
        cookie: str,
        app_id,
        app_type,
        distributor_id,
        msg_name: str,
        msg_type: int,
        send_time: str,
        send_target: int,
        content,
):
    """
    运营配置-客服消息-新建消息
    目前仅支持文字消息
    :param token: x-secsdk-csrf-token
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param msg_name: 消息名称
    :param msg_type: 消息类型：1-文字消息，2-图文消息
    :param content: 消息内容，
    文字消息：f'<p>{text_content}</p>'，
    图文消息：{
            'img_uri': img_uri,
            'img_url': img_url,
            'link_html': link_html,
            'msg_url': msg_url,
            'title': title,
            'url_title': url_title,
        }
    :param send_time: 发送时间，例如：2022-12-31 17:27:33
    :param send_target: 发送用户，1-全部用户，2-已充值用户，3-未充值用户
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/customer_service_message/create/v1/'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Origin": "https://www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "content-type": "application/json",
        "distributorid": str(distributor_id),
        'x-secsdk-csrf-token': token
    }
    data = {
        "msg_name": msg_name,
        "msg_type": msg_type,
        "send_time": send_time,
        "send_target": send_target
    }
    if msg_type == 1:
        data['msg_detail'] = {
            "content": content  # 消息内容
        }
    elif msg_type == 2:
        data['msg_detail'] = content
    else:
        return
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=data,
        headers=headers,
        return_json=True
    )


def wx_get_page_url(
        cookie: str,
        token: str,
        app_id,
        app_type,
        distributor_id
):
    """
    位置：（H5书城分销）运营配置-客服消息-新建消息-消息链接（页面链接）
    功能：获取页面链接列表
    :param cookie: cookie
    :param token: token
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/wx/get_page_url/v1/'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id),
        "x-secsdk-csrf-token": token
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def wx_get_activity_list(
        cookie: str,
        app_id,
        app_type,
        distributor_id,
        page: int = 1,
        page_size: int = 10
):
    """
    位置：（H5书城分销）运营配置-客服消息-新建消息-消息链接（插入活动链接）
    功能：获取 活动链接列表
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param page: 页码
    :param page_size: 每页数量
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/get_activity_list/v1/'
    params = {
        'activity_type': 2,  # 看似固定
        'activity_status': "1,2,3",  # 看似固定
        'page_index': page - 1,
        'page_size': page_size,
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id)
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def customer_service_message_upload(
        token: str,
        cookie: str,
        app_id,
        app_type,
        distributor_id,
        file_dir
):
    """
    位置：（H5书城分销）运营配置-客服消息-新建消息-消息图片
    功能：上传图片
    :param token: x-secsdk-csrf-token
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param file_dir: 需要上传的文件路径
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/customer_service_message/upload/v1/'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Origin": "https://www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id),
        'x-secsdk-csrf-token': token
    }
    files = [
        ('file', (open(file_dir, 'rb')))
    ]
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        files=files,
        return_json=True
    )


def application_overview_list_v1(
        cookie: str,
        token: str,
        app_id: int,
        app_type: int,
        distributor_id: int = 0,
        begin_date: str = None,
        end_date: str = None,
        is_optimizer_view: bool = False,
        date_type: int = 1,
        page: int = 1,
        page_size: int = 10
):
    """
    位置：（H5书城分销）数据统计-应用统计
    功能：获取数据
    :param cookie: cookie
    :param token: token
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param begin_date: 开始时间，例如：20230715
    :param end_date: 结束时间，例如：20230721
    :param is_optimizer_view:
    :param date_type: 日维度的时候为1，月维度的时候为2
    :param page:
    :param page_size:
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/application_overview_list/v1'

    params = {
        'is_optimizer_view': is_optimizer_view,
        'date_type': date_type,
        'inner_app_id': app_id,
        'page_index': page - 1,
        'page_size': page_size
    }
    if begin_date:
        params['begin'] = begin_date.replace('-', '')
    else:
        params['begin'] = lazytime.get_date_string(days=-7).replace('-', '')
    if end_date:
        params['end'] = end_date.replace('-', '')
    else:
        params['end'] = lazytime.get_date_string(days=0).replace('-', '')

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Referer": "https://www.changdunovel.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id),
        "x-secsdk-csrf-token": token
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def promotion_overview_v1(
        cookie: str,
        token: str,
        app_id: int,
        app_type: int,
        distributor_id: int = 0,
        begin_date: str = None,
        end_date: str = None,
        page: int = 1,
        page_size: int = 10
):
    """
    位置：（H5书城分销）数据统计-推广统计-推广链接明细
    功能：获取数据
    :param cookie: cookie
    :param token: token
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param begin_date: 开始时间，例如：2023-07-18
    :param end_date: 结束时间，例如：2023-07-24
    :param page:
    :param page_size:
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/promotion_overview/v1'

    params = {
        'begin_date': begin_date,
        'end_date': end_date,
        'page_index': page - 1,
        'page_size': page_size
    }
    if begin_date:
        params['begin_date'] = begin_date
    else:
        params['begin_date'] = lazytime.get_date_string(days=-15)
    if end_date:
        params['end_date'] = end_date
    else:
        params['end_date'] = lazytime.get_date_string(days=0)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Referer": "https://www.changdunovel.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id),
        "x-secsdk-csrf-token": token
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def apps_from_login_v1(
        cookie: str,
        token: str
):
    """
    获取apps列表，所有的
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/login/v1/'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Referer": "https://www.changdunovel.com/sale/monitor/center",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "x-secsdk-csrf-token": token
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )
