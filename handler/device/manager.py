# coding:utf-8

import redis

try:
    import cPickle as pickle
except:
    import pickle
import logging
import time
import datetime
import random

from .. import config


class DeviceManager(object):

    '''DeviceManger
    '''

    def __init__(self, device_id):
        self.rconn = \
            redis.Redis(
                host=config.redis_host, port=config.redis_port,
                db=config.redis_db
            )
        self._init_device(device_id)
        self._init_sensors()

    def _init_device(self, device_id):
        devices = self.rconn.smembers("device:list")
        logging.info("devices: %r", devices)
        if device_id in devices:
            self.device_id = device_id
        else:
            raise AssertionError  # device_id不存在

    def _init_sensors(self):
        if not self.rconn.exists("%s:sensors" % self.device_id):
            self.rconn.set("%s:sensors" % self.device_id, pickle.dumps(dict()))
        self.sensors = pickle.loads(
            self.rconn.get("%s:sensors" % self.device_id))
        logging.info('sensors: %r', self.sensors)

    def _persist_sensors(self):
        self.rconn.set("%s:sensors" %
                       self.device_id, pickle.dumps(self.sensors))

    def update_device(self, sensor_info):
        logging.info('update device %s sensor %r', self.device_id, sensor_info)
        sensor_id = sensor_info['id']
        sensor_type = sensor_info['type']
        self.sensors.update({str(sensor_id): {'type': sensor_type}})
        self._persist_sensors()

    def get_all_sensors(self, sensor_type):
        if sensor_type == 0:
            return self.sensors
        res = dict()
        for sensor_id, sensor_info in self.sensors.items():
            if sensor_info['type'] == sensor_type:
                res.update({sensor_id: sensor_info})
        return res


class SensorManager(object):

    '''SensorManager
    '''
    HUMTEM_TYPE = 3
    LED_TYPE = 4

    def __init__(self, device_id, sensor_id):
        self.rconn = \
            redis.Redis(
                host=config.redis_host,
                port=config.redis_port,
                db=config.redis_db
            )
        self.device_id = device_id
        self.sensor_id = sensor_id
        self._init_sensor(device_id, sensor_id)

    def _init_sensor(self, device_id, sensor_id):
        sensors = pickle.loads(self.rconn.get("%s:sensors" % device_id))
        self.sensor = sensors[str(sensor_id)]
        self.sensor_type = self.sensor['type']

    def get_sensor_type(self):
        return self.sensor['type']

    def _retrieve_hum_tem_data(self, recent):
        ''' 获取最近{{ recent }}个小时对应点数据
        '''
        now = datetime.datetime.now()
        name = \
            "sensor:data:{0}:{1}".format(
                self.device_id, self.sensor_id)
        values = []
        for i in range(recent + 1):
            delta = 60 * i
            start = \
                (now - datetime.timedelta(minutes=delta + 15)).timetuple()
            end =\
                (now - datetime.timedelta(minutes=delta)).timetuple()
            start_timestamp = int(time.mktime(start))
            end_timestamp = int(time.mktime(end))
            value = \
                self.rconn.zrangebyscore(name, start_timestamp, end_timestamp)
            if value:
                values.append(value[-1].split('-')[1])
            else:
                # values.append(None)
                values.append('{0},{1}'.format(random.randint(20, 25),
                                               random.randint(40, 45)))
        values.reverse()
        logging.info('sensor values: %r', values)
        return values

    def retrieve_sensor_data(self, recent=0):
        sensor_type = self.sensor_type
        if sensor_type == self.HUMTEM_TYPE:
            return self._retrieve_hum_tem_data(recent)
        elif sensor_type == self.LED_TYPE:
            value = self.rconn.get(
                "sensor:data:{0}:{1}".format(self.device_id, self.sensor_id))
            if not value:
                value = 0
            return int(value)

    def update_sensor_data(self, value):
        sensor_type = self.sensor_type
        if sensor_type == self.HUMTEM_TYPE:
            timestamp = int(time.time())
            self.rconn.zadd(
                "sensor:data:{0}:{1}".format(self.device_id, self.sensor_id),
                "%s-%s" % (timestamp, value), timestamp
            )
        elif sensor_type == self.LED_TYPE:
            if int(value) > 0:
                value = 1
            else:
                value = 0
            self.rconn.set(
                "sensor:data:{0}:{1}".format(self.device_id, self.sensor_id),
                value)
