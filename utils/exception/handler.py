#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：handler.py
@Author  ：宇宙大魔王
@Date    ：2021/6/17 15:20 
@Desc    ：
"""
from bases.response import APIResponse


def api_exception_handler(exc, context):
    """
    自定义异常返回接口格式
    :param exc:
    :param context:
    :return:
    """

    return APIResponse(exc)

