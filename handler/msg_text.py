# coding:utf-8

import time
import hashlib
import logging
import json

import config
from libs import mcurl


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
            config.tuling_robot_api, config.tuling_robot_api, info, userid)

        robot_resp = mcurl.CurlHelper().get(chat_robot_url)
        logging.info('receive %s from tuling_robot' % (robot_resp))
        robot_resp_dic = json.loads(robot_resp)

        resp_msg = robot_resp_dic['text']
        curr_timestamp = int(time.time())
        return config.TextTpl % (self.from_user,
                                 self.to_user, curr_timestamp, resp_msg)
