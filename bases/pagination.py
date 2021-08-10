#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera
@File    ：pagination.py
@Author  ：宇宙大魔王
@Date    ：2021/6/9 17:58
@Desc    ：继承Drf的PageNumberPagination类，使用自定义的APIResponse统一接口返回数据的格式
"""
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination

from bases.response import APIResponse


class APIPageNumberPagination(PageNumberPagination):
    """
    继承Drf的PageNumberPagination类，分页内容格式继续使用原始的方式
    可以不再继承直接使用，也可以继承使用
    """

    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        """
        1、重写，使用自定义APIResponse返回响应数据
        2、增加pages，展示总页数
        :param data:
        :return:
        """
        return APIResponse(OrderedDict([
            ('count', self.page.paginator.count),
            ('pages', self.get_page_nums()),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_page_nums(self):
        """
        自定义方法，计算当前page size下总页数
        :return:
        """
        if self.page_size is None:
            page_size = self.request.GET.get(self.page_size_query_param)

            if page_size:
                self.page_size = int(page_size)
            else:
                self.page_size = 9

        count = self.page.paginator.count
        modulo = count % self.page_size
        quotient = count / self.page_size
        pages = int(quotient) if modulo == 0 else int(quotient) + 1
        return pages


class APISimplePagination(APIPageNumberPagination):
    """
    继承APIPageNumberPagination，省去多余数据，只响应该页数中的数据
    可以不再继承直接使用，也可以继承使用
    """

    def get_paginated_response(self, data):
        """
        1、重写，使用自定义APIResponse返回响应数据
        2、简化接口数据内容
        3、增加pages，展示总页数
        :param data:
        :return:
        """
        return APIResponse(data, pages=self.get_page_nums())
