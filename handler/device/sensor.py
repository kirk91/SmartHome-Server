# coding:utf-8

import tornado.web
import redis
import json
import rpyc

from .. import config
from .manager import SensorManager


class Sensor(object):
    '''
    '''
    SENSOR_HUM = 1
    SENSOR_TEM = 2
    SENSOR_HUMTEM = 3
    SENSOR_LED = 4


class SensorHandler(tornado.web.RequestHandler):
    '''SensorDataHandler
    传感器数据的控制中心
    '''

    def __init__(self, *args, **kwargs):
        super(SensorHandler, self).__init__(*args, **kwargs)
        self.rconn = \
            redis.Redis(
                host=config.redis_host,
                port=config.redis_port,
                db=config.redis_db
            )


    def get(self, device_id, sensor_id):
        sensor_manager = SensorManager(device_id, sensor_id)
        sensor_type = sensor_manager.get_sensor_type()
        if sensor_type == 4:
            self.render('sensor_led.html', title='led',
                        sensor_id=sensor_id,)
        elif sensor_type == 3:
            self.render('sensor_tem.html', title='humtem',
                        sensor_id=sensor_id,)

    def put(self, device_id, sensor_id):
        sensor_type = self.manager.get_sensor_type(device_id, sensor_id)
        data = json.loads(self.request.data)
        value = data['value']
        if sensor_type == 4:
            self.manager.retrieve_sensor_data( value)
        elif sensor_type == 3:
            command = \
                {'device_id': device_id,
                 'sensor_id': sensor_id,  # 0表示开启所有的led
                 'value': value}

            conn = rpyc.connect('127.0.0.1', 8889)
            conn.root.handle_msg(json.dumps(command))
            conn.close()
