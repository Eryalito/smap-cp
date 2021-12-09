from device import Device


def DevicesToDict(devices: list) -> dict:
    newDevices = []
    for device in devices:
        newDevices.append(device.__dict__)
    return newDevices


def DictToDevices(devices: dict) -> list:
    newDevices = []
    for deviceDict in devices:
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
        newDevices.append(device)
    return newDevices
