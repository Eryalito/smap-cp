from json.encoder import JSONEncoder
from device import Device
from step import Step


class encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def DevicesToDict(devices: list) -> dict:
    newDevices = encoder().encode(devices)
    return newDevices


def DictToDevices(devices: dict) -> list:
    newDevices = []
    for deviceDict in devices:
        if not (
            ('id' in deviceDict or '_id' in deviceDict)
            and
            ('key' in deviceDict or '_key' in deviceDict)
        ):
            raise ValueError('Invalid device found')
        id = deviceDict['id'] if 'id' in deviceDict else deviceDict['_id']
        key = deviceDict['key'] if 'key' in deviceDict else deviceDict['_key']
        ip = deviceDict['ip'] if 'ip' in deviceDict else deviceDict['_ip']
        vers = deviceDict['version'] if 'vresion' in deviceDict else (
            deviceDict['_version'] if '_vresion' in deviceDict else '3.3')
        name = deviceDict['name'] if 'name' in deviceDict else (
            deviceDict['_name'] if '_name' in deviceDict else id)
        steps = []
        if 'steps' in deviceDict or '_steps' in deviceDict:
            stepsDict = deviceDict['steps'] if 'steps' in deviceDict else deviceDict['_steps']
            if type(stepsDict) == list:
                for stepDict in stepsDict:
                    step = Step(
                        start=int(stepDict['start']
                                  ) if 'start' in stepDict else
                        (int(stepDict['_start']
                             ) if '_start' in stepDict else 0),
                        end=int(stepDict['end'])
                        if 'end' in stepDict else
                        (int(stepDict['_end'])
                         if '_end' in stepDict else 24),
                        count=int(stepDict['count'])
                        if 'count' in stepDict else
                        (int(stepDict['_count'])
                         if '_count' in stepDict else 0)
                    )
                    steps.append(step)
        device = Device(identifier=id, key=key, ip=ip,
                        version=vers, name=name, steps=steps)
        newDevices.append(device)
    return newDevices
