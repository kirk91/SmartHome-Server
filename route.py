#! /usr/bin/env python
# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import handler

urls = [
        (r'/',handler.index.IndexHandler),
        (r'/weixin',handler.weixin.WechatHandler),
        ]
