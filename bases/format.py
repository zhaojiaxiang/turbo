#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera
@File    ：api_format.py
@Author  ：宇宙大魔王
@Date    ：2021/6/10 13:48 
@Desc    ：通用接口返回格式
"""


def api_format(code, result, data, exception='', *args, **kwargs):
    dic = {'code': code, 'result': result, 'data': data, 'exception': exception}
    dic.update(kwargs)
    return dic
