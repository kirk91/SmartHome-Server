# coding: utf-8

import json


class TlMsg(object):

    '''Tuling Message
    '''

    MSG_TEXT_TYPE = 100000
    MSG_LINK_TYPE = 200000
    MSG_TRAIN_TYPE = 305000
    MSG_FLIGHT_TYPE = 306000

    def __init__(self, msg):
        self.msg = json.loads(msg)
        self.msg_code = self.msg['code']

    def parse(self):
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
