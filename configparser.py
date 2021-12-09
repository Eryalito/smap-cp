import yaml
from yaml.loader import Loader
from device import Device


class ConfigParser:
    def __init__(self, path: str):
        self._path = path

    def Load(self) -> dict:
        a_yaml_file = open(self._path)
        return yaml.load(a_yaml_file, Loader=yaml.FullLoader)

    def ToDevices(self, devicesDict: dict) -> list:
        devices = []
        for deviceDict in devicesDict:
            if('id' not in deviceDict or
               'key' not in deviceDict or 'ip' not in deviceDict):
                raise ValueError('Invalid device found')
            id = deviceDict['id']
            key = deviceDict['key']
            ip = deviceDict['ip']
            vers = deviceDict['version'] if 'vresion' in deviceDict else '3.3'
            name = deviceDict['name'] if 'name' in deviceDict else id
            device = Device(identifier=id, key=key, ip=ip,
                            version=vers, name=name)
            devices.append(device)
        return devices
