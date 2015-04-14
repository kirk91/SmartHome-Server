#! /usr/bin/env python
# coding:utf-8

import redis
import config
import time
import rpyc
import json
import logging


class EventMsg(object):

    def __init__(self, msg):
        self.redis = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUserName")
        self.from_user = msg.get("FromUserName")

    def handle(self):
        event_action = {
            "subscribe": self._subscribe,
            "unsubscribe": self._unsubscribe,
            "SCAN": self._scan,
            "scancode_push": self._scan_push,
            "scancode_waitmsg": self._scan_waitmsg,
            "CLICK": self._click,
            "VIEW": self._view,
            "LOCATION": self._location,
        }

        resp_msg, resp_msg_type = event_action.get(self.event)()
        curr_timestamp = int(time.time())

        if resp_msg_type == 'text':
            return config.TextTpl % \
                (self.from_user, self.to_user, curr_timestamp, resp_msg)

    def _subscribe(self):
        if self.redis.sismember("wx_user:list", self.from_user):
            user_id = int(
                self.redis.hget("wx_user:%s" % self.from_user, 'uid'))
            if 'EventKey' in self.msg and self.msg.get('EventKey'):
                event_key = self.msg.get('EventKey')[8:]
                # 暂时一个用户只能绑定一个树莓派
                self.redis.hset("user:%d" % user_id, "device_id", event_key)
                return ('恭喜您已经成功绑定家居客户端，可以试试下方菜单', 'text')

        else:
            user_id = self.redis.incr("user:id")
            self.redis.sadd("user:list", user_id)
            self.redis.sadd("wx_user:list", self.from_user)
            self.redis.hset("wx_user:%s" % self.from_user, 'uid', user_id)
            self.redis.hset("user:%d" % user_id, "openid", self.from_user)

            if 'EventKey' in self.msg and self.msg.get('EventKey'):
                event_key = self.msg.get('EventKey')[8:]
                # 暂时一个用户只能绑定一个树莓派
                self.redis.hset("user:%d" % user_id, "device_id", event_key)
                return ('感谢关注家居小助手！您已经成功绑定家居客户端，可以试试下方菜单', 'text')

            return ('感谢关注家居小助手！为了提供更方便的服务，您需要绑定客户端', 'text')

    def _unsubscribe(self):
        return ('成功取消关注', 'text')  # 先不删除用户

    def _scan_waitmsg(self):
        event_key = self.msg.get('EventKey')
        if event_key == 'BIND':
            scan_code_info = self.msg['ScanCodeInfo']
            scan_res = scan_code_info['ScanResult']
            if scan_res and self.redis.exists(scan_res):
                device_id = int(self.redis.get(scan_res))
                if device_id:
                    self._bind(device_id)
                    return '恭喜您已成功绑定设备', 'text'
                else:
                    return '设备违法, 请使用原厂设备', 'text'
            else:
                logging.info('%r' % scan_code_info)
                return '%s %s' % \
                    (scan_code_info['ScanType'],
                     scan_code_info['ScanResult']), 'text'
        else:
            return event_key, 'text'

    def _scan_push(self):
        return '', 'text'

    def _bind(self, device_id):
        user_id = int(self.redis.hget("wx_user:%s" % self.from_user, 'uid'))
        self.redis.hset("user:%d" % user_id, "device_id", device_id)
        logging.info('user:%s bind device:%s' % (user_id, device_id))

    def _scan(self):
        # 这里缺少用户绑定新的树莓派客户端的检测
        device_id = self.msg.get('EventKey')
        self._bind(device_id)

        return ('恭喜你已经成功绑定家居客户端', 'text')

    def _click_light(self, event_key, device_id):
        if event_key == 'LIGHT_ON':
            value = 1
        elif event_key == 'LIGHT_OFF':
            value = 0
        command = {'device_id': device_id,
                   'sensor_id': 0,  # 0表示开启所有的led
                   'value': value}

        conn = rpyc.connect('127.0.0.1', 8889)
        res = conn.root.handleMessage(json.dumps(command))
        conn.close()

        if res:
            return 'open the light', 'text'
        else:
            return '客户端未接入互联网或者已断线', 'text'

    def _click_humtem(self):
        pass

    def _click_mydevice(self, device_id):
        return '您的设备id为%s' % device_id, 'text'

    def _click(self):
        event_key = self.msg.get('EventKey', '')
        uid = int(self.redis.hget("wx_user:%s" % self.from_user, 'uid'))

        if self.redis.hexists("user:%d" % uid, "device_id"):
            device_id = int(self.redis.hget("user:%d" % uid, "device_id"))
            if event_key == 'MY_DEVICE':
                return self._click_mydevice(device_id)
            elif event_key == 'REAL_TEMPERATURE':
                self._click_humtem()
            elif event_key == 'LIGHT_ON' or \
                    event_key == 'LIGHT_OFF':
                self._click_light(event_key, device_id)
            else:
                return ('%s暂时还没有定义, 正在开发中...' % event_key, 'text')
        else:
            return ('您还为绑定家居客户端，请先绑定', 'text')

    def _view(self):
        pass

    def _location(self):
        pass
