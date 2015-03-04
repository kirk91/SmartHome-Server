#! /usr/bin/env python
# coding:utf-8

import redis
import config
import time
import rpyc
import json

class EventMsg(object):
    def __init__(self,msg):
        self.redis = redis.Redis(host = config.redis_host, port = config.redis_port, db = config.redis_db)
        self.msg = msg
        self.event = msg.get("Event")
        self.to_user = msg.get("ToUserName")
        self.from_user = msg.get("FromUserName")


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
         curr_timestamp = int(time.time())

         if resp_msg_type == 'text':
            return config.TextTpl % (self.from_user,self.to_user,curr_timestamp,resp_msg)

    def Subscribe(self):
        if self.redis.sismember("wx_user:list", self.from_user):
            user_id = int(self.redis.hget("wx_user:%s"%self.from_user, 'uid'))
            if self.msg.has_key('EventKey') and self.msg.get('EventKey'):
                event_key = self.msg.get('EventKey')[8:]
                # 暂时一个用户只能绑定一个树莓派
                self.redis.hset("user:%d"%user_id, "device_id", event_key)
                return ('恭喜您已经成功绑定家居客户端，可以试试下方菜单','text')

        else:
            user_id = self.redis.incr("user:id")
            self.redis.sadd("user:list",user_id)
            self.redis.sadd("wx_user:list",self.from_user)
            self.redis.hset("wx_user:%s"%self.from_user, 'uid',user_id)
            self.redis.hset("user:%d"%user_id, "openid", self.from_user)

            if self.msg.has_key('EventKey') and self.msg.get('EventKey'):
                event_key = self.msg.get('EventKey')[8:]
                # 暂时一个用户只能绑定一个树莓派
                self.redis.hset("user:%d"%user_id, "device_id", event_key)
                return ('感谢关注家居小助手！您已经成功绑定家居客户端，可以试试下方菜单','text')

            return ('感谢关注家居小助手！为了提供更方便的服务，您需要绑定客户端','text')

    def  UnSubscribe(self):
        # 先不删除用户
        return ('成功取消关注','text')

    def Scan(self):
        # 这里缺少用户绑定新的树莓派客户端的检测
        event_key = self.msg.get('EventKey')
        user_id = int(self.redis.hget("wx_user:%s"%self.from_user, 'uid'))
        self.redis.hset("user:%d"%user_id, "device_id", event_key)

        return ('恭喜你已经成功绑定家居客户端','text')

    def Click(self):
        event_key = self.msg.get('EventKey','')
        uid = int(self.redis.hget("wx_user:%s"%self.from_user,'uid'))

        if self.redis.hexists("user:%d"%uid, "device_id"):
            device_id = int(self.redis.hget("user:%d"%uid,"device_id"))
            conn = rpyc.connect('127.0.0.1', 8889)
            if event_key == 'LIGHT_ON' or event_key == 'LIGHT_OFF' or event_key == 'REAL_TEMPERATURE':
                req_msg = {'uid':uid,'device_id':device_id,'key':event_key,'info':event_key}
                res = conn.root.handleMessage(json.dumps(req_msg))
                conn.close()
                res_dict = json.loads(res)
                status = res_dict['status']
                if status == -1:
                    return ('客户端未接入互联网或者已断线','text')
                elif status == 0:
                    return (res_dict['info'],'text')
            else:
                # other key
                pass
        else:
            return ('您还为绑定家居客户端，请先绑定','text')

    def View(self):
        pass

    def Location(self):
        pass
