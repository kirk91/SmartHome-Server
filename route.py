#! /usr/bin/env python
# coding:utf-8

import handler

urls = [
    (r'/', handler.index.IndexHandler),
    (r'/weixin', handler.weixin.WechatHandler),
    (r'/weixin/oauth', handler.oauth.OauthHandler)
    (r'/wexin/auth', handler.oauth.AuthHandler)
    (r'/device/qr', handler.qr.QrcodeHandler),
    (r'/device/sensor/data', handler.device.DataHandler),
    (r'/device/new', handler.device.DeviceInfoHandler),
]
