#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：handlers.py
@Author  ：宇宙大魔王
@Date    ：2021/6/8 17:50 
@Desc    ：通用程序处理集合
"""


class SerializerValidateHandler:
    """
    在Serializer中使用validate方法进行字段验证时使用该类
    handle_validation负责收集错误字段以及错误信息
    show_validation负责将错误字典返回并由ValidationError抛出
    """
    def __init__(self):
        self.error_dict = {}

    def handle_validation(self, field, message):
        temp_list = [message]
        self.error_dict[field] = temp_list

    def has_validation(self):
        return True if len(self.error_dict) > 0 else False

    def show_validation(self):
        return self.error_dict
