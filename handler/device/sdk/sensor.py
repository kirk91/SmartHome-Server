# coding:utf-8

from ..manager import DeviceManager, SensorManager


class Sensor(object):
    '''Sensor sdk
    '''
    def __init__(self, device_id):
        self.device_id = device_id
        self._init_sensors(device_id)

    def _init_sensors(self, device_id):
        device_manager = DeviceManager(device_id)
        self.sensors = \
            device_manager.get_all_sensors(SensorManager.HUMTEM_TYPE)
        self.sensor_id = self.sensors()[0]

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
