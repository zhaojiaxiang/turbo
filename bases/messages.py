#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：messages.py
@Author  ：宇宙大魔王
@Date    ：2021/6/11 15:42 
@Desc    ：
"""

from django.utils.translation import ugettext_lazy as _

# 默认处理成功时返回的信息
MSG_20000_OK = _("ok")
# 自定义ViewSet在增删改查时，处理成功时返回的信息
MSG_20001_RETRIEVE_OK = _("retrieve ok")
MSG_20002_CREATE_OK = _("create ok")
MSG_20003_UPDATE_OK = _("update ok")
MSG_20004_DELETE_OK = _("delete ok")

# 在使用ModelSerializer或者Serializer进行表单验证时，验证失败时返回的信息
# 所有数据验证失败默认返回的信息
MSG_30000_VALIDATE_NG = _("validate ng")
# form、Serializer验证失败返回的信息
MSG_30001_FORM_VALIDATE_NG = _("form validate ng")
# 业务验证失败返回的信息
MSG_30002_BUSINESS_VALIDATE_NG = _("business validate ng")

# 默认在处理失败时返回的信息
MSG_40000_NG = _("ng")
# 自定义ViewSet在增删改查时，处理失败时返回的信息
# 主键资源不存在
MSG_40001_RETRIEVE_NG = _("retrieve ng")
# 数据库插入错误
MSG_40002_CREATE_NG = _("create ng")
# 数据库更新错误
MSG_40003_UPDATE_NG = _("update ng")
# 数据库删除错误
MSG_40004_DELETE_NG = _("delete ng")
# Not Found错误，同MSG_40001_RETRIEVE_NG类似
MSG_40005_NOT_FOUND = _("not found")
# Method Not Allowed错误
MSG_40006_METHOD_NOT_ALLOWED = _("method %s not allowed")

# 用户相关处理失败时返回的信息
# 用户不存在
MSG_50001_ERROR_USER = _("error user")
# 密码不正确
MSG_50002_ERROR_PASS = _("error password")
# 用户已失效
MSG_50003_NOT_VALID = _("user invalid")
# 用户未认证
MSG_50004_UNAUTHORIZED = _("user unauthorized")
# 用户认证失败
MSG_50005_AUTHENTICATION_FAILED = _("user authentication failed")
# 用户无权限
MSG_50006_PERMISSION_DENIED = _("user permission denied")
# Token失效
MSG_50007_TOKEN_INVALID = _("token is invalid or expired")

# 数据库异常时返回的信息
MSG_60000_DB_NG = _("db ng")
MSG_60001_DB_UNIQUE_NG = _("db unique ng")