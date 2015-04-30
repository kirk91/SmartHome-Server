#! /usr/bin/env python
# coding:utf-8

import tornado.web
import json
import logging

from .manager import DeviceManager, SensorManager


class DeviceHandler(tornado.web.RequestHandler):

    '''DeviceHandler
    '''

    def __init__(self, *args, **kwargs):
        super(DeviceHandler, self).__init__(*args, **kwargs)

    def get(self, device_id):
        sensor_type = int(self.get_argument('type', 0))
        device_manager = DeviceManager(device_id)
        sensors = device_manager.get_all_sensors(sensor_type)
        logging.info(sensors)
        sensors = sorted(sensors.items(), key=lambda x: x[0])
        logging.info(sensors)

        humtem_sensors = []
        led_sensors = []
        tags = ['Home', 'Parlor', 'Bedroom', 'Kitchen']
        index = 0
        for sid, sinfo in sensors:
            stype = sinfo['type']
            tag = tags[index]
            index += 1
            sensor_manager = SensorManager(device_id, sid)
            if stype == sensor_manager.HUMTEM_TYPE:
                value = sensor_manager.retrieve_sensor_data()[0]   # 温度，湿度
                humtem_sensors.append(
                    {
                        "id": sid,
                        "tag": tag,
                        "value": value
                    }
                )
            elif stype == sensor_manager.LED_TYPE:
                value = sensor_manager.retrieve_sensor_data()
                led_sensors.append(
                    {
                        "id": sid,
                        "tag": tag,
                        "value": value
                    }
                )

        self.render(
            'sensors.html', device_id=device_id,
            humtem_sensors=humtem_sensors,
            led_sensors=led_sensors)

    def put(self, device_id):
        logging.info('receive device info: %r', self.request.body)
        data = json.loads(self.request.body)
        sensor_id, sensor_type = \
            data['sensor_id'], data['sensor_type']
        sensor_info = {'id': sensor_id, 'type': sensor_type}
        device_manager = DeviceManager(device_id)
        device_manager.update_device(sensor_info)
        self.write('update device info')
