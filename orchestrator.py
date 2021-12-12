import utils
from cache.cachemanager import CacheManager
from database.smapdb import SMAPDB
import threading
import datetime
import re


class Orchestrator:
    
    def __init__(self, cacheManager: CacheManager, db: SMAPDB) -> None:
        self._cacheManager = cacheManager
        self._db = db
        
    def start(self) -> None:
        self.executeOnce()
        threading.Timer(int(self._cacheManager.GetValue('timer_time')), self.start).start()
        
    def executeOnce(self) -> None:
        today = datetime.datetime.today().weekday()
        # Load devices
        devicesDict = self._cacheManager.GetSerializable('devices')
        devices = utils.DictToDevices(devicesDict)        
        for device in devices:
            for step in device.steps:
                fro = 0
                to = 6
                if re.search(pattern='^[0-9]{1}(-[0-9]){1}$', string=step.days) is not None:
                    fro = int(step.days.split('-')[0])
                    to = int(step.days.split('-')[1])
                if today >= fro and today <= to:
                    pass
        