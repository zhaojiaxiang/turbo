#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：turbo 
@File    ：handler.py
@Author  ：宇宙大魔王
@Date    ：2021/7/16 15:31 
@Desc    ：
"""

from django.db import connections, connection


def db_connection_execute(sql_str, as_type=None):

    with connection.cursor() as cursor:
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        if as_type == "dict":
            columns = [col[0].lower() for col in cursor.description]

            result = [
                dict(zip(columns, row))
                for row in rows
            ]
            return result
        return rows


def man_power_connection_execute(sql_str):

    with connections['ManPower'].cursor() as cursor:
        cursor.execute(sql_str)
        rows = cursor.fetchall()
    return rows


def query_single_with_no_parameter(sql_string, as_type=None):
    """
    查询单个字段通用方法
    :param sql_string:
    :param as_type: list 说明是以list的格式返回结果
    :return:
    """
    rows = db_connection_execute(sql_string)

    if as_type == "list":
        return exchange_result_to_list(rows)

    return rows


def exchange_result_to_list(rows):
    """
    将查询到的结果转换为list，适用于单字段查询
    :param rows:
    :return:
    """
    result_list = []
    for row in rows:
        result_list.append(row[0])

    return result_list
