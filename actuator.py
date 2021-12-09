import tinytuya
from device import Device


class Actuator:
    def __init__(self, device: Device):
        self._device = device
        self._outlet = tinytuya.OutletDevice(device.id, device.ip, device.key)
        if device.version == '3.3':
            self._outlet.set_version(3.3)

    # Turn on the device for the given seconds. 0 make it on forever
    def TurnOn(self, seconds: int = 0):
        self._outlet.set_status(True, 1)
        self._outlet.set_timer(seconds)
