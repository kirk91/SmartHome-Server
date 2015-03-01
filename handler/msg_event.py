#! /usr/bin/env python
# coding:utf-8

import redis
import config
import time

class EventMsg(object):
    def __init__(self,msg):
        self.redis = redis.Redis(host = config.redis_host, port = config.redis_port, db = config.redis_db)
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUsername")
        self.from_user = msg.get("FromUsername")


    def handle(self):
         event_action = {
             "subscribe" : self.Subscribe,
             "unsubscribe": self.UnSubscribe,
             "SCAN" : self.Scan,
             "CLICK": self.Click,
             "VIEW": self.View,
             "LOCATION": self.Location,
         }

         resp_msg,resp_msg_type = event_action.get(self.event)()
         curr_timestamp = int(time.tim())

         if resp_msg_type == 'text':
            return config.TextTpl % (self.from_user,self.to_user,curr_timestamp,resp_msg)

    def Subscribe(self):
        user_id = self.redis.incr("users:id")
        self.redis.sadd("users:list",user_id)
        self.redis.hset("weixin:%s"%self.from_user, 'uid',user_id)
        self.redis.hset("users:%d"%user_id, "openid", self.from_user)

        if self.msg.has_key('EventKey') and self.msg.get('EventKey'):
            event_key = self.msg.get('EventKey')[8:]
            # 暂时一个用户只能绑定一个树莓派
            self.redis.hset("users:%d"%user_id, "device_id", event_key)
            return ('感谢关注家居小助手！您已经成功绑定家居客户端，可以试试下方菜单','text')

        return ('感谢关注家居小助手！为了提供更方便的服务，您需要绑定客户端','text')

    def  UnSubscribe(self):
        pass

    def Scan(self):
        event_key = self.msg.get('EventKey')
        user_id = self.redis.hget("weixin:%s"%self.from_user, 'uid')
        self.redis.hset("users:%d"%user_id, "device_id", event_key)

        return ('恭喜你已经成功绑定家居客户端','text')

    def Click(self):
        pass

    def View(self):
        pass

    def Location(self):
        pass
