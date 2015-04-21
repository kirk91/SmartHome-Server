# coding:utf-8

import tornado.web
import redis

from .. import config


class DeviceHandler(tornado.web.RequestHandler):
    '''
    '''
    def __init__(self, *args, **kwargs):
        super(DeviceHandler, self).__init__(*args, **kwargs)
        self.rconn = \
            redis.Redis(
                host=config.redis_host, port=config.redis_port,
                db=config.redis_db
            )

    def get(self, uid):
        device_id = int(self.rconn.hget("user:%s" % uid, "device_id"))
        devices = [device_id]
        self.render('devices.html', items=devices)
