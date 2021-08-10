#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：turbo 
@File    ：serializers.py
@Author  ：宇宙大魔王
@Date    ：2021/7/16 13:55 
@Desc    ：
"""
from rest_framework import serializers

from rbac.models import Role, Group, Organizations


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ("name", )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("name", )


class OrganizationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizations
        fields = ("name", "isgroup")
