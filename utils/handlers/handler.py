#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：turbo 
@File    ：handler.py
@Author  ：宇宙大魔王
@Date    ：2021/7/16 16:21 
@Desc    ：
"""
from utils.db.handler import query_single_with_no_parameter


def get_all_organization_belong_me(request):
    user = request.user

    if user.organization.isgroup:

        str_sql = f"select getallchildlist({user.organization.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')
    else:
        str_sql = f"select getallchildlist({user.organization.parent.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')

    if len(organization) == 1:
        # 由于元组中只有一个元素时，会有一个‘,’，因此让元组中有两个一样的元素
        organization = organization + organization

    return tuple(organization)


def get_all_organizations(organization):

    str_sql = f"select getallchildlist({organization})"
    organization_list = query_single_with_no_parameter(str_sql, 'list')
    organization = organization_list[0].split(',')

    if len(organization) == 1:
        # 由于元组中只有一个元素时，会有一个‘,’，因此让元组中有两个一样的元素
        organization = organization + organization

    return tuple(organization)


def get_all_organization_group_belong_me(request):
    user = request.user

    if user.organization.isgroup:

        str_sql = f"select getchildgrouplist({user.organization.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')
    else:
        organization = [user.organization.parent.id]

    if len(organization) == 1:
        # 由于元组中只有一个元素时，会有一个‘,’，因此让元组中有两个一样的元素
        organization = organization + organization

    return tuple(organization)
