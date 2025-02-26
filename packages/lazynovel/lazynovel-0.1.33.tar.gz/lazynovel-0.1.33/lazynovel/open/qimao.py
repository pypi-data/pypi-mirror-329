#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
from lazysdk import lazyrandom
from lazysdk import lazyenv
import hashlib
import time

default_start_time = 1735660800  # 2025-01-01 00:00:00
"""
开发文档：https://x0sgcptncj.feishu.cn/docx/H0iBdZuUEox7rQxSLMBcQ4upnpc

模块介绍：
    1、七猫平台的开放接口封装的sdk，方便快速使用；
    2、目前支持的产品类型为：抖音小程序、微信小程序，需要注意project一定要填写正确；

使用方法：
    Basics类封装了生成签名的方法和基础接口的调用方法，使用类之前要实例化，然后调用即可；
"""


class Basics:
    """
    基础类，用来实现基本的功能，单个账号的情况下可以直接使用，多账号的情况下建议使用外部的快捷方法。
    """

    def __init__(
            self,
            admin_account_name: str,
            access_key: str,
            secret_key: str,
            project: int = 8,
    ):
        """
        :param admin_account_name: 总账号用户名
        :param access_key: 【必填】开发者账号的access_key
        :param secret_key: 【必填】开发者账号的secret_key
        :param project: 分销项目标识：6-抖音小程序，8-微信小程序
        """
        self.admin_account_name = admin_account_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.project = project

    def make_sign(
            self,
            data: dict = None
    ) -> str:
        """
        签名算法，
        :param data: 需要制作签名的数据
        生成sign，校验码
        """
        if data is None:
            data = {}
        random = lazyrandom.random_str(str_length=8)  # 随机数
        timestamp = int(time.time())  # 发起请求时的时间戳，秒
        if "admin_account_name" not in data.keys():
            data["admin_account_name"] = self.admin_account_name
        if "project" not in data.keys():
            data["project"] = self.project
        if "access_key" not in data.keys():
            data["access_key"] = self.access_key
        if "random" not in data.keys():
            data["random"] = random
        if "timestamp" not in data.keys():
            data["timestamp"] = timestamp

        keys = list(data.keys())
        keys.sort()  # 升序排序
        key_value_list = []
        for key in keys:
            if key == 'sign':
                # 忽略sign字段
                pass
            else:
                value = data.get(key)
                key_value = '%s=%s' % (key, value)
                key_value_list.append(key_value)
        data_str = "&".join(key_value_list) + self.secret_key  # 在拼接后的字符串上加上secret_key
        d5 = hashlib.md5()
        d5.update(data_str.encode(encoding='UTF-8'))  # 然后对字符串md5
        return d5.hexdigest().lower()  # 返回小写的校验码

    def query_order(
            self,
            admin_account_name: str,
            project: int = 8,
            app_id: str = None,
            trade_create_time_start: int = None,  # 按照订单的创建时间进行查询,查询的时间范围的开始时间，时间戳，秒,trade_create_time_start 默认为7天前
            trade_create_time_end: int = None,  # 按照订单的创建时间进行查询, trade_create_time_end 默认为当前时间
            trade_finish_time_start: int = None,  # 按照订单的完成时间进行查询
            trade_finish_time_end: int = None,  # 按照订单的完成时间进行查询

            page: int = 1,
            page_size: int = 100
    ):
        """
        5.3.1 获取用户订单明细列表
        注：
            1.此接口有调用频率限制，相同查询条件每秒仅能请求一次
            2.单页返回 100 条数据
            3.查询的时间段不能超过 7 天
        :param admin_account_name: 总账号用户名
        :param project: 分销项目标识，必传
        :param app_id: 小程序appid
        :param trade_create_time_start: 按照订单的创建时间进行查询；查询的时间范围的开始时间，时间戳，秒；与 trade_create_time_end 跨度最多7天（7*86400秒）
        :param trade_create_time_end: 按照订单的创建时间进行查询；查询的时间范围的结束时间，时间戳，秒
        :param trade_finish_time_start: 按照订单的完成时间进行查询；查询的时间范围的开始时间，时间戳，秒
        :param trade_finish_time_end: 按照订单的完成时间进行查询；查询的时间范围的结束时间，时间戳，秒
        :param page: 页码
        :param page_size: 每页条数，默认100；范围为[1,100]

        """
        url = 'https://new-media-mapi.qimao.com/mapi/v1/order/list'
        params = {
            "page": page,
            "page_size": page_size,
        }
        if admin_account_name:
            params["admin_account_name"] = admin_account_name
        if project:
            params["project"] = project
        if app_id:
            params["appid"] = app_id
        if trade_create_time_start:
            params["trade_create_time_start"] = trade_create_time_start
        if trade_create_time_end:
            params["trade_create_time_end"] = trade_create_time_end
        if trade_finish_time_start:
            params["trade_finish_time_start"] = trade_finish_time_start
        if trade_finish_time_end:
            params["trade_finish_time_end"] = trade_finish_time_end
        params_sign = self.make_sign(data=params)
        params["sign"] = params_sign
        response = lazyrequests.lazy_requests(
            url=url,
            method='GET',
            params=params,
            return_json=True
        )
        return response


def query_order(
        project: int = 8,
        app_id: str = None,
        trade_create_time_start: int = None,
        trade_create_time_end: int = None,
        trade_finish_time_start: int = None,
        trade_finish_time_end: int = None,
        page: int = 1,
        page_size: int = 100,

        env_file: str = None,
        admin_account_name: str = None,
        access_key: str = None,
        secret_key: str = None
):
    """
    5.3.1 获取用户订单明细列表
        注：
            1.此接口有调用频率限制，相同查询条件每秒仅能请求一次
            2.单页返回 100 条数据
            3.查询的时间段不能超过 7 天
        :param admin_account_name: 总账号用户名
        :param project: 分销项目标识，必传
        :param app_id: 小程序appid
        :param trade_create_time_start: 按照订单的创建时间进行查询；查询的时间范围的开始时间，时间戳，秒；与 trade_create_time_end 跨度最多7天（7*86400秒）
        :param trade_create_time_end: 按照订单的创建时间进行查询；查询的时间范围的结束时间，时间戳，秒
        :param trade_finish_time_start: 按照订单的完成时间进行查询；查询的时间范围的开始时间，时间戳，秒
        :param trade_finish_time_end: 按照订单的完成时间进行查询；查询的时间范围的结束时间，时间戳，秒
        :param env_file:
        :param access_key:
        :param secret_key:
        :param page: 页码
        :param page_size: 每页条数，默认100；范围为[1,100]

    """
    # ------------------- 初始化 -------------------
    if not admin_account_name and not access_key and not secret_key and env_file:
        env_info = lazyenv.read(env_file)
        admin_account_name = env_info.get("admin_account_name")
        access_key = env_info.get("access_key")
        secret_key = env_info.get("secret_key")
    else:
        pass

    local_basic = Basics(
        admin_account_name=admin_account_name,
        access_key=access_key,
        secret_key=secret_key
    )  # 实例化
    # ------------------- 初始化 -------------------
    return local_basic.query_order(
        admin_account_name=admin_account_name,
        project=project,
        app_id=app_id,
        trade_create_time_start=trade_create_time_start,
        trade_create_time_end=trade_create_time_end,
        trade_finish_time_start=trade_finish_time_start,
        trade_finish_time_end=trade_finish_time_end,
        page=page,
        page_size=page_size
    )
