# coding:utf-8

import config
import time

class TextMsg(object):
    def __init__(self,msg):
        self.msg = msg
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.content = msg.get('Content')

    def handle(self):
            curr_timestamp = int(time.time())
            resp_msg = self.content
            return config.TextTpl % (self.from_user,self.to_user,curr_timestamp,resp_msg)

