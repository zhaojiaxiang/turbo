#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：code.py
@Author  ：宇宙大魔王
@Date    ：2021/6/4 15:54 
@Desc    ：自定义系统级别识别代码
"""

# 默认处理成功时返回的代码
CODE_20000_OK = 20000
# 自定义ViewSet在增删改查时，处理成功时返回的代码
CODE_20001_RETRIEVE_OK = 20001
CODE_20002_CREATE_OK = 20002
CODE_20003_UPDATE_OK = 20003
CODE_20004_DELETE_OK = 20004

# 在使用ModelSerializer或者Serializer进行表单验证时，验证失败时返回的代码
# 所有数据验证失败默认返回的代码
CODE_30000_VALIDATE_NG = 30000
# form、Serializer验证失败返回的代码
CODE_30001_FORM_VALIDATE_NG = 30001
# 业务验证失败返回的代码
CODE_30002_BUSINESS_VALIDATE_NG = 30002

# 默认在处理失败时返回的代码
CODE_40000_NG = 40000
# 自定义ViewSet在增删改查时，处理失败时返回的代码
# 主键资源不存在
CODE_40001_RETRIEVE_NG = 40001
# 数据库插入错误
CODE_40002_CREATE_NG = 40002
# 数据库更新错误
CODE_40003_UPDATE_NG = 40003
# 数据库删除错误
CODE_40004_DELETE_NG = 40004
# Not Found错误，同CODE_40001_RETRIEVE_NG类似
CODE_40005_NOT_FOUND = 40005
# Method Not Allowed错误
CODE_40006_METHOD_NOT_ALLOWED = 40006

# 用户相关处理失败时返回的代码
# 用户不存在
CODE_50001_ERROR_USER = 50001
# 密码不正确
CODE_50002_ERROR_PASS = 50002
# 用户已失效
CODE_50003_NOT_VALID = 50003
# 用户未认证
CODE_50004_UNAUTHORIZED = 50004
# 用户认证失败
CODE_50005_AUTHENTICATION_FAILED = 50005
# 用户无权限
CODE_50006_PERMISSION_DENIED = 50006
# Token失效
CODE_50007_TOKEN_INVALID = 50007

# 数据库异常时返回的代码
CODE_60000_DB_NG = 60000
CODE_60001_DB_UNIQUE_NG = 60001
