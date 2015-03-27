# coding:utf-8

import time
import hashlib
import logging

import config
from libs import mcurl
from . import tl_msg


class TextMsg(object):

    def __init__(self, msg):
        self.msg = msg
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.content = msg.get('Content')

    def handle(self):
        info = self.content
        md5 = hashlib.md5()
        md5.update(self.from_user)
        userid = md5.hexdigest()
        chat_robot_url = '%s?key=%s&info=%s&userid=%s' % (
            config.tuling_robot_api, config.tuling_robot_key, info, userid)

        robot_resp = mcurl.CurlHelper().get(chat_robot_url)
        logging.info('receive %s from tuling_robot' % (robot_resp))

        resp_msg, resp_msg_type = tl_msg.TlMsg(robot_resp).handle()
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
