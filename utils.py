import datetime
import time
from json.encoder import JSONEncoder
from typing import List

import pytz

from device import Device
from step import Step

TIMEZONE = 'UTC'


class encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def TimestampToUnix(timestamp: str, timezone: str = TIMEZONE) -> float:
    return time.mktime(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(timezone)).timetuple())

def UnixToDatetime(unix: float, timezone: str = TIMEZONE) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(unix).astimezone(pytz.timezone(timezone))

def UnixToTimestamp(unix: float, timezone: str = TIMEZONE) -> str:
    return UnixToDatetime(unix, timezone).strftime('%Y-%m-%d %H:%M:%S')

def DayTimestamp(t: float, timezone: str = TIMEZONE) -> str:
    return datetime.datetime.fromtimestamp(t).replace(tzinfo=pytz.timezone(timezone)).strftime('%Y-%m-%d')

def DayUnix(t: float, timezone: str = TIMEZONE) -> float:
    t = datetime.datetime.strptime(datetime.datetime.fromtimestamp(t).astimezone(pytz.timezone(timezone)).strftime('%Y-%m-%d'), '%Y-%m-%d')
    t = t.replace(tzinfo=pytz.timezone(timezone)).astimezone(tz=None)
    return time.mktime(t.timetuple())

def DevicesToDict(devices: List[Device]) -> dict:
    newDevices = encoder().encode(devices)
    return newDevices


def DictToDevices(devices: dict) -> List[Device]:
    newDevices = []
    for deviceDict in devices:
        if not (('id' in deviceDict or '_id' in deviceDict) and ('key' in deviceDict or '_key' in deviceDict)):
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
                        days=stepDict['days'] if 'days' in stepDict else stepDict['_days'] if '_days' in stepDict else '0-6',
                        start=int(stepDict['start']
                                  ) if 'start' in stepDict else
                        (int(stepDict['_start']
                             ) if '_start' in stepDict else 0),
                        end=int(stepDict['end'])
                        if 'end' in stepDict else
                        (int(stepDict['_end'])
                         if '_end' in stepDict else 24),
                        count=float(stepDict['count'])
                        if 'count' in stepDict else
                        (float(stepDict['_count'])
                         if '_count' in stepDict else 0),
                        timezone=stepDict['timezone'] if 'timezone' in stepDict else stepDict['_timezone'] if '_timezone' in stepDict else 'CET'
                    )
                    steps.append(step)
        device = Device(identifier=id, key=key, ip=ip,
                        version=vers, name=name, steps=steps)
        newDevices.append(device)
    return newDevices
