#! /usr/bin/env python
# coding:utf-8

import tornado.web
import redis
import json
import time
import logging

import config


class DataHandler(tornado.web.RequestHandler):
    '''SensorDataHandler
    传感器数据的控制中心
    '''

    def __init__(self, *args, **kwargs):
        super(DataHandler, self).__init__(*args, **kwargs)
        self.redis = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=config.redis_db)

    def get(self):
        device_id = self.get_argument('device_id')
        sensor_id = self.get_argument('sensor_id')
        start = self.get_argument('start', '')
        end = self.get_argument('end', '')

        now = time.time()
        if not start:
            start = now - 3600
        if not end:
            end = now

        info = self.redis.zrangebyscore('data:%s:%s' % (device_id, sensor_id),
                                        start, end, withscores=True)
        logging.info('%r', info)

    def post(self):
        data = json.loads(self.request.body)
        timestamp = time.time()
        device_id, sensor_id, value = data['device_id'], data['sensor_id'], \
            data['value']

        self.redis.zadd('data:%s:%s' % (device_id, sensor_id),
                        value, timestamp)

        self.write('data has stored')


class DeviceCenter(object):
    '''DeviceCenter
    '''
    DEVICES = list()
    SENSORS = dict()

    def __init__(self):
        self.redis = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self._get_all_devices()
        self.SENSORS = dict()

    def _get_all_devices(self):
        self.DEVICES = self.redis.smembers("device:list")

    def update_device_info(self, device_id, sensor_info):
        logging.info('update device %s sensor %r', device_id, sensor_info)
        if device_id not in self.SENSORS:
            self.SENSORS[device_id] = list()

        sensor_id = sensor_info['id']
        sensor_type = sensor_info['type']
        self.SENSORS[device_id].append({'id': sensor_id,
                                        'type': sensor_type})

    def get_device_info(self, device_id):
        return self.SENSORS[device_id]


device_center = DeviceCenter()


class DeviceInfoHandler(tornado.web.RequestHandler):
    '''DeviceInfoHandler
    '''

    def __init__(self, *args, **kwargs):
        super(DeviceInfoHandler, self).__init__(*args, **kwargs)

    def get(self):
        device_id = self.get_argument('device_id')
        info = device_center.get_device_info(device_id)

        self.write(json.dumps(info))

    def post(self):
        logging.info('receive device info: %r', self.request.body)
        data = json.loads(self.request.body)
        device_id, sensor_id, sensor_type = data['device_id'],\
            data['sensor_id'], data['sensor_type']
        sensor_info = {'id': sensor_id, 'type': sensor_type}
        device_center.update_device_info(device_id, sensor_info)

        self.write('update device info')
