#! /usr/bin/env python
# coding:utf-8

import tornado.web

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import config
import hashlib
import logging
try:
    from xml.etree import cElementTree as ET
except:
    from xml.etree import ElementInclude as ET
import msg_event
import msg_text

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

            msg = self.parse_request_xml(self.request.body)
            msg_type = msg.get('MsgType')
            msg_action = {
                "event" : msg_event.EventMsg,
                "text" : msg_text.TextMsg,
            }

            msg_handler = msg_action.get(msg_type)(msg)
            resp_msg = msg_handler.handle()
            logging.info(resp_msg)
            self.write(resp_msg)
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

    def parse_request_xml(self,xml_str):
        msg = dict()
        root = ET.fromstring(xml_str)
        if root.tag == 'xml':
            for child in root:
                msg[child.tag] = child.text
        return msg

