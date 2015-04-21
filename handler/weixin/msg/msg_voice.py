# coding: utf-8

import time

from . import tl_msg
from ... import config


class VoiceMsg(object):
    '''Voice Msg
    '''
    def __init__(self, msg):
        self.msg = msg
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.content = msg.get('Recognition')

    def handle(self):
        resp_msg, resp_msg_type = \
            tl_msg.TlMsg(self.from_user, self.content).get()
        curr_timestamp = int(time.time())

        if resp_msg_type == 'text':
            return config.TextTpl % (self.from_user, self.to_user,
                                     curr_timestamp, resp_msg)
        elif resp_msg_type == 'multitext':
            items = ''
            for content in resp_msg:
                items += config.MultiItemTpl % (
                    content['title'], content['description'],
                    content['picurl'], content['url'])
            return config.MultiTextTpl % (self.from_user, self.to_user,
                                          curr_timestamp, len(resp_msg), items)
