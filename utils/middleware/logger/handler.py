#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：handler.py
@Author  ：宇宙大魔王
@Date    ：2021/6/22 16:13 
@Desc    ：日志中间件，摘自网上，做了一些修改
"""
import datetime
import json
import os
import time

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from turbo.settings import LOG_PATH

WHITE_LIST_URL = ['media', 'static']


def _get_request_headers(request):
    headers = {}
    for k, v in request.META.items():
        if k.startswith('HTTP_'):
            headers[k[5:].lower()] = v
    return headers


def _get_response_headers(response):
    headers = {}
    headers_tuple = response.items()
    for i in headers_tuple:
        headers[i[0]] = i[1]
    return headers


class CollectionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            if request.path[1:].split('/')[0] not in WHITE_LIST_URL:
                request_body = dict(request.POST)

                if request_body:
                    request.META['REQUEST_BODY'] = request_body
                else:
                    try:
                        request_body = json.loads(
                            str(request.body, encoding='utf-8').replace(' ', '').replace('\n', '').replace('\t', ''))
                        request.META['REQUEST_BODY'] = request_body
                    except:
                        request.META['REQUEST_BODY'] = {}

                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    remote_address = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    remote_address = request.META['REMOTE_ADDR']
                request.META['IP'] = remote_address
                # 获取请求的 username，如果是未登录的则为 AnonymousUser
                if not isinstance(request.user, AnonymousUser):
                    user = request.user.username
                else:
                    user = 'AnonymousUser'
                request.META['USER'] = user
                request.META['REQUEST_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        except Exception as ex:
            write_log(repr(ex))

    def process_response(self, request, response):
        try:
            if request.path[1:].split('/')[0] not in WHITE_LIST_URL:
                if not isinstance(request.user, AnonymousUser):
                    user = request.user.username
                else:
                    user = 'AnonymousUser'
                request.META['USER'] = user

                # 获取响应内容
                if response['content-type'] == 'application/json':
                    if getattr(response, 'streaming', False):
                        response_body = '<<<Streaming>>>'
                    else:
                        response_body = json.loads(str(response.content, encoding='utf-8'))
                else:
                    try:
                        response_body = response.data if response.status_code == 200 else response.reason_phrase
                    except:
                        response_body = response.reason_phrase
                request.META['RESP_BODY'] = response_body

                # 获取请求的 view 视图名称
                try:
                    request.META['VIEW'] = request.resolver_match.view_name
                except AttributeError:
                    request.META['VIEW'] = None

                request.META['STATUS_CODE'] = response.status_code
                request.META['RESPONSE_TIME'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        except Exception as ex:
            write_log(repr(ex))
        finally:
            return response


class LoggerMiddleware(MiddlewareMixin):
    """
    中间件，记录日志
    """

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        try:
            if request.path[1:].split('/')[0] not in WHITE_LIST_URL:
                log_data = {
                    'request': {
                        'timestamp': request.META['REQUEST_TIME'],
                        'user': request.META['USER'],
                        'method': request.method,
                        'path': request.get_full_path(),
                        'body': request.META['REQUEST_BODY'],
                        'view': request.META['VIEW'],
                        'ip': request.META['IP'],
                        'headers': _get_request_headers(request),
                    },
                    'response': {
                        'timestamp': request.META['RESPONSE_TIME'],
                        'status': request.META['STATUS_CODE'],
                        'body': request.META['RESP_BODY'],
                        'headers': _get_response_headers(response),
                    },
                }
                write_log(str(log_data))
        except Exception as ex:
            write_log(repr(ex))
        finally:
            return response


def write_log(log_info):
    timestamp = time.localtime(time.time())
    log_path = os.path.join(LOG_PATH, time.strftime('%Y-%m', timestamp))
    create_folder(log_path)
    log_name = time.strftime('%Y-%m-%d', timestamp) + '.log'

    full_log_path = os.path.join(log_path, log_name)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open(full_log_path, 'a', encoding='utf-8') as f:
        f.write(str(current_time) + ' : ' + log_info + '\n')


def create_folder(upload_path):
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
