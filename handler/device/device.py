#! /usr/bin/env python
# coding:utf-8

import tornado.web
import json
import logging

from .manager import DeviceManager


class DeviceHandler(tornado.web.RequestHandler):
    '''DeviceHandler
    '''
    def __init__(self, *args, **kwargs):
        super(DeviceHandler, self).__init__(*args, **kwargs)
        self.manager = DeviceManager()


    def get(self, device_id):
        sensor_type = int(self.get_argument('type', 0))
        sensors = self.manager.get_all_sensors(device_id, sensor_type)
        logging.info(sensors)


        self.render('sensors.html', device_id=device_id, sensors=sensors)

    def put(self, device_id):
        logging.info('receive device info: %r', self.request.body)
        data = json.loads(self.request.body)
        sensor_id, sensor_type = \
            data['sensor_id'], data['sensor_type']
        sensor_info = {'id': sensor_id, 'type': sensor_type}
        self.manager.update_device(device_id, sensor_info)
        self.write('update device info')
