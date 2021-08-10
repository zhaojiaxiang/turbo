#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：response.py
@Author  ：宇宙大魔王
@Date    ：2021/6/4 15:44 
@Desc    ：继承DRF的Response，自定义响应的数据格式；Http状态码固定为200，并加入自定义业务状态码。
"""
from django.db import IntegrityError, DatabaseError
from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound, ValidationError, \
    AuthenticationFailed, MethodNotAllowed
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from bases import results, messages
from bases import codes
from bases.format import api_format


class APIResponse(Response):
    """
    继承DRF中Response，增加参数，并将参数写入到data中
    result为OK时，data中数据为接口有效数据
    result为NG时，data.exception为异常数据，如果code==CODE_30000_VALIDATE_NG，则data.exception为字典对象，否则为字符串
    """

    def __init__(self, data=None, status=None, headers=None, code=codes.CODE_20000_OK, result=results.RESULT_OK, *args,
                 **kwargs):

        exception = ""

        # DRF Simple JWT InvalidToken
        if isinstance(data, InvalidToken):
            data = str(messages.MSG_50007_TOKEN_INVALID)
            result = results.RESULT_NG
            code = codes.CODE_50007_TOKEN_INVALID

        # Django rest-framework exceptions
        if isinstance(data, MethodNotAllowed):
            data = str(messages.MSG_40006_METHOD_NOT_ALLOWED % data.args[0])
            result = results.RESULT_NG
            code = codes.CODE_40006_METHOD_NOT_ALLOWED

        if isinstance(data, NotAuthenticated):
            data = str(messages.MSG_50004_UNAUTHORIZED)
            result = results.RESULT_NG
            code = codes.CODE_50004_UNAUTHORIZED

        if isinstance(data, AuthenticationFailed):
            data = str(messages.MSG_50005_AUTHENTICATION_FAILED)
            result = results.RESULT_NG
            code = codes.CODE_50005_AUTHENTICATION_FAILED

        if isinstance(data, PermissionDenied):
            data = str(messages.MSG_50006_PERMISSION_DENIED)
            result = results.RESULT_NG
            code = codes.CODE_50006_PERMISSION_DENIED

        if isinstance(data, NotFound):
            data = str(messages.MSG_40005_NOT_FOUND)
            result = results.RESULT_NG
            code = codes.CODE_40005_NOT_FOUND if code == codes.CODE_20000_OK else code

        if isinstance(data, ValidationError):
            data = self.convert_exception(data)
            result = results.RESULT_NG
            code = codes.CODE_30000_VALIDATE_NG

        # Django exceptions
        if isinstance(data, Http404):
            data = str(messages.MSG_40001_RETRIEVE_NG)
            result = results.RESULT_NG
            code = codes.CODE_40001_RETRIEVE_NG if code == codes.CODE_20000_OK else code

        if isinstance(data, IntegrityError):
            data = str(messages.MSG_60001_DB_UNIQUE_NG)
            result = results.RESULT_NG
            code = codes.CODE_60001_DB_UNIQUE_NG

        # DatabaseError为IntegrityError的基类
        if isinstance(data, DatabaseError):
            data = f"Error no:{str(data.args[0])}, error message:{data.args[1]}"
            result = results.RESULT_NG
            code = codes.CODE_60000_DB_NG

        # 以上异常无法处理时执行
        if isinstance(data, Exception):
            data = repr(data)
            result = results.RESULT_NG
            code = codes.CODE_40000_NG

        if isinstance(data, str):
            result = results.RESULT_NG if result == results.RESULT_OK else result
            code = codes.CODE_40000_NG if code == codes.CODE_20000_OK else code

        if result == results.RESULT_NG:
            exception = data
            data = None

        if data is None:
            data = {}

        dic = api_format(code=code, result=result, data=data, exception=exception, *args, **kwargs)

        super().__init__(data=dic, status=status, headers=headers)

    def convert_exception(self, exc):
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                data = exc.detail
            else:
                data = str(exc.detail[0])
            return data
        return repr(exc)
