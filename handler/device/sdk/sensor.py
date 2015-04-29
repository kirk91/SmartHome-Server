# coding:utf-8

import logging

from ..manager import DeviceManager, SensorManager


class Sensor(object):
    '''Sensor sdk
    '''
    def __init__(self, device_id, sensor_type):
        self.device_id = device_id
        self.sensor_type = sensor_type
        self._init_sensors(device_id)

    def _init_sensors(self, device_id):
        device_manager = DeviceManager(str(device_id))
        self.sensors = \
            device_manager.get_all_sensors(self.sensor_type)
        logging.info('sensors: %r', self.sensors)
        if self.sensors:
            self.sensor_id = self.sensors.keys()[0]
        else:
            self.sensor_id = None

    def get(self):
        if self.sensors:
            manager = SensorManager(self.device_id, self.sensor_id)
            sensor_type = manager.get_sensor_type()
            if sensor_type == manager.HUMTEM_TYPE:
                values = manager.retrieve_sensor_data(recent=5)
                return values
            else:
                return None  # other sensor return none
        else:
            return None
