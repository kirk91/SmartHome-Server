#! /usr/bin/env python
# coding:utf-8

from route import urls

import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__),"template"),
    static_path = os.path.join(os.path.dirname(__file__),"static")
    )

app = tornado.web.Application(
    handlers = urls,
    **settings
    )

