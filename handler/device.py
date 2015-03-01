#! /usr/bin/env python
# coding:utf-8

import os

import tornado.web

import redis
import mcurl
import config
import json

class QrcodeHandler(tornado.web.RequestHandler):
    def __init__(self,*argc,**argkw):
        tornado.web.RequestHandler.__init__(self,*argc,**argkw)
        self.redis = redis.Redis(host = config.redis_host, port = config.redis_port, db = config.redis_db)
        self.curl = mcurl.CurlHelper()

    def get(self):
        q = self.get_argument('q','query')
        user = self.get_argument('admin','')

        if q=='query':
            device_id = int(self.get_argument('device_id',0))
            if self.redis.sismember("device:list", device_id):
                qr_ticket = self.redis.hget("device:%d"%device_id, "qr_ticket")
                self.write('<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" width=250px>'% qr_ticket)
            else:
                self.write("Device does not exist !!!")
        elif q == 'generate' and user == 'hanliang' :
            device_id = self.redis.incr("device:id")
            self.redis.sadd("device:list",device_id)
            access_token = self.getAccessToken()
            post_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": device_id}}}
            res = self.curl.post('https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s',(access_token,),json.dumps(post_data))
            res_dict = json.loads(res)
            qr_ticket  = res_dict.get('ticket')
            qr_url = res_dict.get('url')
            self.redis.hset("device:%d" % device_id, 'qr_ticket', qr_ticket)
            self.redis.hset("device:%d" % device_id, 'qr_url', qr_url)

            #向客户端返回图片
            self.write('<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" width=250px>'% qr_ticket)
        else:
            self.write('hello, welcome to device center !')


    def getAccessToken(self):
        if self.redis.exists("weixin_accesstoken"):
            return self.redis.get("weixin_accesstoken")
        else:
            # 重新获取accesstoken并存入redis
            res = self.curl. get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s',(config.appid,config.appsecret))
            res_dict = json.loads(res)
            self.redis.set("weixin_accesstoken", res_dict.get("access_token"), res_dict.get("expires_in",7200))
            return  res_dict.get("access_token")

