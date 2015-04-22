# coding: utf-8

import json
import logging
import hashlib

from ... import config
from ...lib import mcurl


class TlMsg(object):

    '''Tuling Message
    '''

    MSG_TEXT_TYPE = 100000
    MSG_LINK_TYPE = 200000
    MSG_TRAIN_TYPE = 305000
    MSG_FLIGHT_TYPE = 306000

    def __init__(self, userid, info):
        self.userid = userid
        self._encrypt_userid()
        self.info = info
        self.curl = mcurl.CurlHelper()

    def _encrypt_userid(self):
        md5 = hashlib.md5()
        md5.update(self.userid)
        self.userid = md5.hexdigest()

    def get(self):
        api_url = '%s?key=%s&info=%s&userid=%s' % (
            config.tuling_robot_api, config.tuling_robot_key,
            self.info, self.userid)
        logging.info(api_url)
        resp = self.curl.get(api_url)
        logging.info('receive %s from tuling_robot' % (resp))
        self.msg = json.loads(resp)
        self.msg_code = self.msg['code']
        return self._parse_msg()

    def _parse_msg(self):
        if self.msg_code == self.MSG_TEXT_TYPE:
            return self.msg['text'], 'text'
        elif self.msg_code == self.MSG_LINK_TYPE:
            return '<a href="%s">%s</a>' % (self.msg['url'], '点击连接查看'), 'text'
        elif self.msg_code == self.MSG_TRAIN_TYPE:
            return self._parse_train()
        elif self.msg_code == self.MSG_FLIGHT_TYPE:
            return self._parse_flight()
        else:
            return '服务器开小差了', 'text'

    def _parse_train(self):
        train_list = self.msg['list'][:6]  # 取前六条信息
        res = list()
        for train in train_list:
            res.append({"title": train['trainnum'],
                        "description": '',
                        "picurl": '%s' % (train['icon'], ),
                        "url": '%s' % (train.get('detailurl', ''), )})
        return res, 'multitext'

    def _parse_flight(self):
        flight_list = self.msg['list'][:6]  # 取前六条信息
        res = list()
        for flight in flight_list:
            res.append({"title": '%s' % (flight['flight']),
                        "description": '',
                        "picurl": flight['icon'],
                        "url": flight.get('detailurl', '')})
        return res, 'multitext'
