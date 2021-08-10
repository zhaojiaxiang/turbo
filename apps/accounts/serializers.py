#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：turbo 
@File    ：serializers.py
@Author  ：宇宙大魔王
@Date    ：2021/7/16 14:05 
@Desc    ：
"""
from rest_framework import serializers

from accounts.models import User
from rbac.serializers import GroupSerializer, RoleSerializer, OrganizationsSerializer


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    roles = RoleSerializer(many=True)
    organization = OrganizationsSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", 'slmsname', 'fmaildays', "avatar",
                  "group", "roles", "organization")


class MyGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "username", "avatar", "email")
