#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：handler.py
@Author  ：宇宙大魔王
@Date    ：2021/6/4 16:21 
@Desc    ：使用Simple JWT进行用户验证，并自定义用户登录验证以及返回接口格式
"""
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.serializers import UserSerializer
from bases import codes, results, messages
from bases.format import api_format

User = get_user_model()


class APITokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录认证，使用自有用户表
    """

    def validate(self, attrs):

        username = attrs['username']
        password = attrs['password']

        code = codes.CODE_20000_OK
        result = results.RESULT_OK

        if re.match('^.+@.+$', username):  # 邮箱登录正则
            user = User.objects.filter(email=username).first()
        else:  # 用户名登录
            user = User.objects.filter(username=username).first()
        if user:
            if user.is_active:
                if user.check_password(password):
                    refresh = self.get_token(user)
                    serializer = UserSerializer(user)
                    data = api_format(code, result, serializer.data, token=str(refresh.access_token),
                                      refresh=str(refresh))
                else:
                    code = codes.CODE_50002_ERROR_PASS
                    result = results.RESULT_NG
                    exception = messages.MSG_50002_ERROR_PASS
                    data = api_format(code, result, {}, exception)
            else:
                code = codes.CODE_50003_NOT_VALID
                result = results.RESULT_NG
                exception = messages.MSG_50003_NOT_VALID
                data = api_format(code, result, {}, exception)
        else:
            code = codes.CODE_50001_ERROR_USER
            result = results.RESULT_NG
            exception = messages.MSG_50001_ERROR_USER
            data = api_format(code, result, {}, exception)
        return data


class APITokenObtainPairView(TokenObtainPairView):
    serializer_class = APITokenObtainPairSerializer


class APITokenRefreshSerializer(TokenRefreshSerializer):
    """
    自定义刷新JWT Token
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        code = codes.CODE_20000_OK
        result = results.RESULT_OK
        refresh = RefreshToken(attrs['refresh'])

        data = api_format(code, result, {}, token=str(refresh.access_token))

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data


class APITokenRefreshView(TokenRefreshView):
    serializer_class = APITokenRefreshSerializer
