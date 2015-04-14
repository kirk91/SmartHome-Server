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

from . import msg_text
from . import msg_event
from . import msg_voice


class WechatHandler(tornado.web.RequestHandler):

    def get(self):
        echostr = self.get_argument('echostr', '')
        if self._checkSignature() and echostr:
            self.write(echostr)
        else:
            self.write('hello,weixin')

    def post(self):
        if self._checkSignature():
            # handle message
            logging.info(self.request.body)

            msg = self._parse_request_xml(self.request.body)
            msg_type = msg.get('MsgType')
            msg_action = {
                "event": msg_event.EventMsg,
                "text": msg_text.TextMsg,
                "voice": msg_voice.VoiceMsg,
            }

            msg_handler = msg_action.get(msg_type)(msg)
            resp_msg = msg_handler.handle()
            logging.info(resp_msg)
            self.write(resp_msg)
        else:
            self.write('hello,weixin')

    def _checkSignature(self):
        signature = self.get_argument('signature', '')
        nonce = self.get_argument('nonce', '')
        timestamp = self.get_argument('timestamp', '')
        tmp_list = [config.token, timestamp, nonce]
        tmp_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, tmp_list)
        hash_code = sha1.hexdigest()
        if hash_code == signature:
            return True
        else:
            return False

    def _parse_request_xml(self, xml_str):
        msg = dict()
        root = ET.fromstring(xml_str)
        if root.tag == 'xml':
            for child in root:
                if child.getchildren():
                    child.text = dict()
                    for subchild in child:
                        child.text[subchild.tag] = subchild.text
                msg[child.tag] = child.text
        return msg
