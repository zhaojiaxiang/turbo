#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera
@File    ：mixins.py
@Author  ：宇宙大魔王
@Date    ：2021/6/4 15:43 
@Desc    ：继承DRF的增删改查Mixin，返回自定义的响应类并加入异常捕获，保证在正确与异常时返回的响应数据格式一致。
"""
from rest_framework import mixins

from bases.response import APIResponse
from bases import codes


class APICreateModelMixin(mixins.CreateModelMixin):
    """
    继承DRF中CreateModelMixin，重写父类的create方法
    """

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return APIResponse(serializer.data, headers=headers, code=codes.CODE_20002_CREATE_OK)
        except Exception as ex:
            return APIResponse(ex, code=codes.CODE_40002_CREATE_NG)


class APIListModelMixin(mixins.ListModelMixin):
    """
    继承DRF中ListModelMixin，重写父类的list方法
    """

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        except Exception as ex:
            return APIResponse(ex, code=codes.CODE_40001_RETRIEVE_NG)
        return APIResponse(serializer.data)


class APIRetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    继承DRF中RetrieveModelMixin，重写父类的retrieve方法
    """

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        except Exception as ex:
            return APIResponse(ex, code=codes.CODE_40001_RETRIEVE_NG)
        return APIResponse(serializer.data)


class APIUpdateModelMixin(mixins.UpdateModelMixin):
    """
    继承DRF中UpdateModelMixin，重写父类的update方法
    """

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as ex:
            return APIResponse(ex, code=codes.CODE_40003_UPDATE_NG)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return APIResponse(serializer.data, code=codes.CODE_20003_UPDATE_OK)


class APIDestroyModelMixin(mixins.DestroyModelMixin):
    """
    继承DRF中DestroyModelMixin，重写父类的destroy方法
    """

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Exception as ex:
            return APIResponse(ex, code=codes.CODE_40004_DELETE_NG)
        return APIResponse(code=codes.CODE_20004_DELETE_OK)
