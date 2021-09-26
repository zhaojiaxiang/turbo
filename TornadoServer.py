#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：turbo 
@File    ：TornadoServer.py
@Author  ：宇宙大魔王
@Date    ：2021/9/26 15:58 
@Desc    ：
"""


import os
import sys
from tornado.options import options, define
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

# Django Application加入查找路径中
app_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(os.path.join(app_path, 'turbo/apps'))
define("port", default=7000, type=int, help="run on the given port")


def main():
    tornado.options.parse_command_line()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turbo.settings')
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    http_server = tornado.httpserver.HTTPServer(wsgi_app, xheaders=True)  # xheaders=True是啥意思？
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
