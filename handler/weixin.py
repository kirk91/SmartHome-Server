#! /usr/bin/env python
# coding:utf-8

import tornado.web

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import config
import hashlib
import logging

class WechatHandler(tornado.web.RequestHandler):
    def get(self):
        echostr = self.get_argument('echostr','')
        if self.checkSignature() and echostr:
            self.write(echostr)
        else:
            self.write('hello,weixin')

    def post(self):
        if self.checkSignature():
            #handle message
            logging.info(self.request.body)
            self.write(self.request.body)
        else:
            self.write('hello,weixin')

    def checkSignature(self):
        signature = self.get_argument('signature','')
        nonce = self.get_argument('nonce','')
        timestamp = self.get_argument('timestamp','')
        tmp_list = [config.token,timestamp,nonce]
        tmp_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, tmp_list)
        hash_code = sha1.hexdigest()
        if hash_code== signature:
            return True
        else:
            return False
