import tinytuya
from device import Device


class TuyaProvider:
    def __init__(self, device: Device):
        self._device = device
        self._outlet = tinytuya.OutletDevice(device.id, device.ip, device.key)
        if device.version == '3.3':
            self._outlet.set_version(3.3)

    # Turn on the device for the given seconds. 0 make it on forever
    def TurnOn(self, seconds: int = 0):
        data = self._outlet.set_status(True, 1)
        if 'Error' in data:
            return False
        self._outlet.set_timer(seconds)
        return True

    def TurnOff(self):
        data = self._outlet.set_status(False, 1)
        return 'Error' not in data
