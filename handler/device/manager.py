# coding:utf-8

import redis
try:
    import cPickle as pickle
except:
    import pickle
import logging
import time

from .. import config


class DeviceManager(object):
    '''DeviceManger
    '''
    def __init__(self):
        self.rconn = \
            redis.Redis(
                host=config.redis_host, port=config.redis_port,
                db=config.redis_db
            )
        self._init_devices()
        self._init_sensors()

    def _init_devices(self):
        self.devices = self.rconn.smembers("device:list")

    def _init_sensors(self):
        if not self.rconn.exists("sensors"):
            self.rconn.set("sensors", pickle.dumps(dict()))
        self.sensors = pickle.loads(self.rconn.get("sensors"))

    def _retrieve_sensors(self):
        self.rconn.set("sensors", pickle.dumps(self.sensors))

    def update_device(self, device_id, sensor_info):
        logging.info('update device %s sensor %r', device_id, sensor_info)
        if device_id not in self.sensors:
            self.sensors[str(device_id)] = dict()

        sensor_id = sensor_info['id']
        sensor_type = sensor_info['type']
        self.sensors[str(device_id)].update(
            {str(sensor_id): {'type': sensor_type}}
        )
        self._retrieve_sensors()

    def get_all_sensors(self, device_id, sensor_type):
        sensors = self.sensors.get(device_id)
        if sensor_type == '':
            return sensors
        res = dict()
        for sensor_id, sensor_info in sensors.items():
            if sensor_info['type'] == sensor_type:
                res.update({sensor_id: sensor_info})
        return res


class SensorManager(object):
    '''SensorManager
    '''
    def __init__(self):
        self.rconn = \
            redis.Redis(
                host=config.redis_host,
                port=config.redis_port,
                db=config.redis_db
            )
        self._init_sensors()

    def _init_sensors(self):
        if not self.rconn.exists("sensors"):
            self.rconn.set("sensors", pickle.dumps(dict()))
        self.sensors = pickle.loads(self.rconn.get("sensors"))

    def get_sensor_type(self, device_id, sensor_id):
        return self.sensors[device_id][sensor_id]['type']

    def retrieve_sensor_data(self, device_id, sensor_id, value):
        # 当前主要用来存储温度湿度
        # value hum,tem
        timestamp = time.time()
        self.rconn.hset("data:{}:{}".format(device_id, sensor_id),
                        value, timestamp
                        )

