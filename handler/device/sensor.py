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
        if sensor_type == sensor_manager.LED_TYPE:
            # self.render('sensor_led.html', title='led',
            # sensor_id=sensor_id,)
            value = sensor_manager.retrieve_sensor_data()
            data = {"id": sensor_id, "type": sensor_type, "value": value}
            self.write(json.dumps(data))
        elif sensor_type == sensor_manager.HUMTEM_TYPE:
            self.render('sensor_tem.html', title='humtem',
                        sensor_id=sensor_id, )

    def put(self, device_id, sensor_id):
        sensor_manager = SensorManager(device_id, sensor_id)
        sensor_type = sensor_manager.get_sensor_type()
        data = json.loads(self.request.body)
        value = int(data['value'])
        sensor_manager.update_sensor_data(value)
        if sensor_type == sensor_manager.HUMTEM_TYPE:
            pass
        elif sensor_type == sensor_manager.LED_TYPE:
            if value > 0:
                value = 1
            else:
                value = 0
            # command = \
            #     {'device_id': device_id,
            #      'sensor_id': sensor_id,  # 0表示开启所有的led
            #      'value': value}
            #
            # conn = rpyc.connect('127.0.0.1', 8889)
            # conn.root.handle_msg(json.dumps(command))
            # conn.close()
            self.write('Update sensor success')