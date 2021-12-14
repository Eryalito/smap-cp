import datetime
import time
from abc import abstractmethod
from typing import List

from record import Record


class SMAPDB():

    def __init__(self) -> None:
        pass

    def _getCurrentTimestamp(self) -> str:
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def _getFirstTimestamp(self) -> str:
        return datetime.datetime.fromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S')

    @abstractmethod
    def init(self) -> bool:
        pass

    @abstractmethod
    def insertRecord(self, timestamp, deviceID: str, seconds: int) -> int:
        pass

    @abstractmethod
    def updateRecord(self, id: int, timestamp, deviceID: str, seconds: int) -> int:
        pass

    @abstractmethod
    def getRecords(self, fro: any = None, to: any = None) -> list:
        pass

    @abstractmethod
    def getRecordsByDevice(self, deviceID: str, fro: any = None, to: any = None) -> List[Record]:
        pass
