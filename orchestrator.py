import datetime
import logging
import math
import re
import time
from binascii import Error

import utils
from cache.cachemanager import CacheManager
from database.smapdb import SMAPDB
from price import Price
from prices.reees import ReeES
from provider.tuyaprovider import TuyaProvider
import pytz


class Orchestrator:

    DAY_LENGTH = 86400
    HOUR_SECONDS = 3600

    def __init__(self, cacheManager: CacheManager, db: SMAPDB) -> None:
        self._cacheManager = cacheManager
        self._db = db
        logging.basicConfig(
            format='%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
            level=logging.INFO,  # Nivel de los eventos que se registran en el logger
        )

    def __dayTimestamp(self, t: float) -> str:
        return datetime.datetime.fromtimestamp(t).astimezone(pytz.timezone(utils.TIMEZONE)).strftime('%Y-%m-%d')

    def __dayUnix(self, t: float):
        t = datetime.datetime.strptime(datetime.datetime.fromtimestamp(t).astimezone(pytz.timezone(utils.TIMEZONE)).strftime('%Y-%m-%d'), '%Y-%m-%d')
        t = t.replace(tzinfo=pytz.timezone(utils.TIMEZONE)).astimezone(tz=None)
        return time.mktime(t.timetuple())

    def _dayTimestamp(self, timestamp) -> float:
        return self.__dayUnix(timestamp)

    def _TSToDT(self, TS: float) -> str:
        return datetime.datetime.fromtimestamp(TS).strftime('%Y-%m-%d %H:%M:%S')

    def start(self) -> None:
        self._sleepTime = int(self._cacheManager.GetValue('timer_time'))
        self.executeOnce()
        time.sleep(self._sleepTime)
        self.start()

    def getPriceForDay(self, day: str):
        cacheResult = None
        prices = []
        try:
            cacheResult = self._cacheManager.GetSerializable('price-' + day)
        except AttributeError:
            pass
        if cacheResult is None:
            code, prices = ReeES().getDataForDay(day)
            if code != 200:
                logging.error('Error fetchinf prices for day ' + day)
                prices = []
            if(len(prices) > 0):
                self._cacheManager.PutSerializable('price-' + day, value=prices)
            return prices
        else:
            for price in cacheResult:
                prices.append(Price(day=price['day'], start=price['start'], length=price['length'], price=price['price']))
            return prices

    def executeOnce(self) -> None:
        today = datetime.datetime.today().weekday()
        now = time.time()
        # Load devices
        devicesDict = self._cacheManager.GetSerializable('devices')
        devices = utils.DictToDevices(devicesDict)
        for device in devices:
            provider = TuyaProvider(device=device)
            for step in device.steps:
                fro = 0
                to = 6
                if re.search(pattern='^[0-9]{1}(-[0-9]){1}$', string=step.days) is not None:
                    fro = int(step.days.split('-')[0])
                    to = int(step.days.split('-')[1])
                if re.search(pattern='^[0-9]{1}$', string=step.days) is not None:
                    fro = int(step.days)
                    to = int(step.days)

                if today >= fro and today <= to:
                    startTS = self._dayTimestamp(now) + step.start * self.HOUR_SECONDS
                    endTS = self._dayTimestamp(now) + step.end * self.HOUR_SECONDS
                    records = self._db.getRecordsByDevice(deviceID=device.id, fro=self._TSToDT(startTS), to=self._TSToDT(endTS if endTS < now else now))
                    totalTime = 0
                    lastRecord = None
                    recordPending = False
                    for record in records:
                        if lastRecord is None:
                            lastRecord = record
                        recordStartTime = utils.TimestampToUnix(record.timestamp)
                        recordDurationS = record.seconds
                        if recordStartTime > utils.TimestampToUnix(lastRecord.timestamp):
                            lastRecord = record
                        recordEstimatedEnd = recordStartTime + recordDurationS
                        if recordEstimatedEnd < now:
                            totalTime += recordDurationS
                        else:
                            recordPending = True

                    if (step.count * self.HOUR_SECONDS) > totalTime:
                        # step not ended, find hours
                        prices = self.getPriceForDay(self.__dayTimestamp(now))
                        # First, filter elements by step hours
                        newPrices = []
                        for price in prices:
                            start = utils.TimestampToUnix(price.start)
                            end = start + price.length
                            if start >= startTS and end <= endTS:
                                newPrices.append(price)
                        # Every price last an hour. Pick just `count` first
                        newPrices.sort(key=lambda x: x.price)
                        newPrices = newPrices[0:int(math.ceil(step.count)) if step.count <= len(newPrices) else len(newPrices)]

                        for price in newPrices:
                            start = utils.TimestampToUnix(price.start)
                            end = start + price.length
                            if now >= start and now < end:
                                # turn on
                                turnOnSeconds = self._sleepTime * 3
                                try:
                                    turnedOn = provider.TurnOn(seconds=turnOnSeconds)
                                    if turnedOn:
                                        if recordPending:
                                            newTime = int(now - utils.TimestampToUnix(lastRecord.timestamp) + turnOnSeconds)
                                            remaining = 0
                                            if newTime > self.HOUR_SECONDS:
                                                remaining = newTime - self.HOUR_SECONDS
                                                newTime = 3600
                                            self._db.updateRecord(id=lastRecord.id, seconds=newTime, timestamp=None, deviceID=None)
                                            if remaining != 0:
                                                self._db.insertRecord(timestamp=self._TSToDT(now), deviceID=lastRecord.deviceID, seconds=remaining)
                                        else:
                                            self._db.insertRecord(timestamp=self._TSToDT(now), deviceID=device.id, seconds=turnOnSeconds)
                                except KeyError:
                                    logging.error('Error turning on the device "' + device.id + ' (' + device.name + ')" forcing stop...')
                                    try:
                                        if provider.TurnOff():
                                            logging.error('Device stopped successfully')
                                        else:
                                            logging.error('Device could not be stopped')
                                    except KeyError:
                                        logging.error('Error trying to stop. The plug could be turn on.')
