# -*- coding: utf-8 -*-
"""
@author: hanyanling
@date: 2025/2/10 17:38
@email:
---------
@summary:
"""
from datetime import datetime, timedelta

import pandas as pd


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kwargs)
        return self._instance[self._cls]


class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


def get_cookies_from_str(cookie_str):
    cookies = {}
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        key, value = cookie.split("=", 1)
        key = key.strip()
        value = value.strip()
        cookies[key] = value

    return cookies


def get_time_range(start_time_str, end_time_str, is_timestamp=False, time_format="%Y-%m-%d"):
    """
    返回给定时间范围内的所有时间，包含开始时间和结束时间。

    :param start_time_str: 开始时间字符串
    :param end_time_str: 结束时间字符串
    :param is_timestamp: 布尔值，如果为True，返回10位时间戳；否则返回格式化的时间字符串
    :param time_format: 时间格式字符串，仅在is_timestamp为False时有效
    :return: 时间日期列表，包含开始时间和结束时间
    """
    # 将字符串转换为datetime对象
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    # 确保开始时间早于结束时间
    if start_time > end_time:
        raise ValueError("开始时间不能晚于结束时间")

    # 计算时间范围内的所有时间
    time_range = []
    current_time = start_time
    while current_time <= end_time:
        if is_timestamp:
            time_range.append(int(current_time.timestamp()))
        else:
            time_range.append(current_time.strftime(time_format))
        current_time += timedelta(days=1)  # 每天一个时间点

    return time_range


def is_empty_data(data):
    """
    判断给定的数据是否为空。

    :param data: 给定的数据
    :return: 如果数据为空，则返回True；否则返回False
    """
    if data is None:
        return True
    if type(data) is pd.DataFrame:
        return data.empty
    if type(data) is pd.Series:
        return data.empty
    if type(data) is list:
        return len(data) == 0
    if type(data) is dict:
        return len(data) == 0
    if type(data) is str:
        return data.strip() == ""
    return False



