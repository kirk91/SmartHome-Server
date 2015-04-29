# coding: utf-8

import time
import rpyc
import json
import datetime
import redis
import logging

from . import tl_msg
from ... import config
from ...device.sdk.sensor import Sensor
from . msg_common import BaseMsg


class VoiceMsg(object):
    '''Voice Msg
    '''
    TEM_COMMAND = "温度"
    HUM_COMMAND = "湿度"
    LED_COMMAND = "电灯"
    OPEN_COMMAND = "开"
    CLOSE_COMMAND = "关"

    def __init__(self, msg):
        self.redis = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self.msg = msg
        self.to_user = msg.get('ToUserName')
        self.from_user = msg.get('FromUserName')
        self.content = msg.get('Recognition').encode('utf-8')

    def handle(self):
        logging.info('Content: %r', self.content)
        uid = int(self.redis.hget("wx_user:%s" % self.from_user, 'uid'))
        if self.redis.hexists("user:%d" % uid, "device_id"):
            device_id = int(self.redis.hget("user:%d" % uid, "device_id"))
        else:
            device_id = None
        if self.TEM_COMMAND in self.content or \
                self.HUM_COMMAND in self.content:
            resp_msg, resp_msg_type = self._handle_hum_tem_msg(device_id)
        elif self.LED_COMMAND in self.content:
            if self.OPEN_COMMAND in self.content:
                resp_msg, resp_msg_type = self._handle_led_msg(device_id, 1)
            elif self.CLOSE_COMMAND in self.content:
                resp_msg, resp_msg_type = self._handle_led_msg(device_id, 0)
            else:
                resp_msg, resp_msg_type = '要关还是开呢', BaseMsg.TEXT_PLAIN
        else:
            resp_msg, resp_msg_type = self._handle_tl_msg()

        curr_timestamp = int(time.time())
        if resp_msg_type == BaseMsg.TEXT_PLAIN:
            return config.TextTpl % (self.from_user, self.to_user,
                                     curr_timestamp, resp_msg)
        elif resp_msg_type == BaseMsg.TEXT_MULTI:
            items = ''
            for content in resp_msg:
                items += config.MultiItemTpl % (
                    content['title'], content['description'],
                    content['picurl'], content['url'])
            return config.MultiTextTpl % (self.from_user, self.to_user,
                                          curr_timestamp, len(resp_msg), items)

    def _handle_tl_msg(self):
        return tl_msg.TlMsg(self.from_user, self.content).get()

    def _handle_hum_tem_msg(self, device_id):
        sensor = Sensor(device_id)
        values = sensor.get()
        resp = list()
        h = int(datetime.datetime.now().hour)
        description = ''
        for value in values:
            if value:
                tem, hum = value.split(',')
                description += '%s点 温度 %s℃ 湿度 %s%%\n' % (h, tem, hum)
            else:
                description += "%s点 暂无温度湿度数据\n" % (h,)
            h -= 1
            if h == -1:
                h = 23

        url = "%s/device/%s/sensor/%s"\
            % (config.domain, device_id, sensor.sensor_id)
        resp.append(
            {
                "title": "温度湿度",
                "description": description,
                "picurl": "",
                "url": url,
            }
        )
        return resp, BaseMsg.TEXT_MULTI

    def _handle_led_msg(self, device_id, value):
        sensor = Sensor(device_id)
        sensor_id = sensor.sensor_id
        command = {'device_id': device_id,
                   'sensor_id': sensor_id,  # 0表示开启所有的led
                   'sensor_value': value}

        conn = rpyc.connect('127.0.0.1', 8889)
        res = conn.root.handle_msg(json.dumps(command))
        conn.close()

        if res:
            if value:
                resp = 'light opened'
            else:
                resp = 'light offed'
            return resp, BaseMsg.TEXT_PLAIN
        else:
            return '客户端未接入互联网或者已断线', BaseMsg.TEXT_PLAIN
