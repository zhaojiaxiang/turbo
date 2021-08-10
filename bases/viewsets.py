#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：viewsets.py
@Author  ：宇宙大魔王
@Date    ：2021/6/4 16:02 
@Desc    ：集成常用Mixin组合
"""
from rest_framework.viewsets import GenericViewSet

from bases import mixins


class APIReadOnlyModelViewSet(mixins.APIRetrieveModelMixin,
                              mixins.APIListModelMixin,
                              GenericViewSet):
    """
    集成只可以读取数据的ViewSet
    """
    pass


class APICreateOnlyViewSet(mixins.APIRetrieveModelMixin,
                           mixins.APIListModelMixin,
                           mixins.APICreateModelMixin,
                           GenericViewSet):
    """
    集成可以新建读取数据的ViewSet
    """
    pass


class APIUpdateOnlyViewSet(mixins.APIRetrieveModelMixin,
                           mixins.APIListModelMixin,
                           mixins.APIUpdateModelMixin,
                           GenericViewSet):
    """
    集成可以更新读取数据的ViewSet
    """
    pass


class APIDeleteOnlyViewSet(mixins.APIRetrieveModelMixin,
                           mixins.APIListModelMixin,
                           mixins.APIDestroyModelMixin,
                           GenericViewSet):
    """
    集成可以删除读取数据的ViewSet
    """
    pass


class APIModelViewSet(mixins.APICreateModelMixin,
                      mixins.APIRetrieveModelMixin,
                      mixins.APIUpdateModelMixin,
                      mixins.APIDestroyModelMixin,
                      mixins.APIListModelMixin,
                      GenericViewSet):
    """
    集成可以对数据进行增删改查的ViewSet
    """
    pass
