# coding:utf-8

import tornado.web
import redis
import json
import rpyc
import datetime

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
            value = sensor_manager.retrieve_sensor_data()
            data = {"id": sensor_id, "type": sensor_type, "value": value}
            self.write(json.dumps(data))
        elif sensor_type == sensor_manager.HUMTEM_TYPE:
            values = sensor_manager.retrieve_sensor_data(recent=24)
            hum_values = []
            tem_values = []
            now_hour = int(datetime.datetime.now().hour)
            labels = []
            for i in range(now_hour, 24):
                labels.append(i)
            for i in range(0, now_hour + 1):
                labels.append(i)

            for value in values:
                if value:
                    tem, hum = value.split(',')
                    tem_values.append(int(tem.strip()))
                    hum_values.append(int(hum.strip()))
                else:
                    tem_values.append(0)
                    hum_values.append(0)
            self.render('sensor_tem.html', title='humtem',
                        sensor_id=sensor_id,
                        tem_data=tem_values,
                        hum_data=hum_values,
                        labels=labels)

    def put(self, device_id, sensor_id):
        sensor_manager = SensorManager(device_id, sensor_id)
        sensor_type = sensor_manager.get_sensor_type()
        data = json.loads(self.request.body)
        value = data['value']
        if sensor_type == sensor_manager.HUMTEM_TYPE:
            sensor_manager.update_sensor_data(value)
            self.write('Update sensor success')
        elif sensor_type == sensor_manager.LED_TYPE:
            value = int(value)
            if value > 0:
                value = 1
            else:
                value = 0
            command = \
                {'device_id': device_id,
                 'sensor_id': sensor_id,
                 'sensor_value': value}

            conn = rpyc.connect('127.0.0.1', 8889)
            res = conn.root.handle_msg(json.dumps(command))
            conn.close()
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            if res:
                sensor_manager.update_sensor_data(value)
                res = {
                    'errcode': 0,
                    'errmsg': '',
                    'msg': 'Update sensor success'
                }
            else:
                res = {
                    'errcode': -1,
                    'errmsg': '客户端未接入互联网或者已断线',
                    'msg': ''
                }
            self.write(json.dumps(res))
