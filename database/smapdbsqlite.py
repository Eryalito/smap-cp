import sqlite3

from record import Record

from database.smapdb import SMAPDB


class SMAPDBSQLite(SMAPDB):

    def __init__(self, file: str, prefix: str) -> None:
        super().__init__()
        self._file = file
        self._prefix = prefix

    def _tableRecords(self) -> str:
        return '`' + self._prefix + 'records`'

    def init(self) -> bool:
        self._connection = sqlite3.connect(self._file)
        cur = self._connection.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS ' + self._tableRecords() + '(id INTEGER PRIMARY KEY AUTOINCREMENT , `timestamp` timestamp not null, deviceID text not null, seconds int not null)')
        self._connection.commit()
        return True

    def insertRecord(self, timestamp, deviceID: str, seconds: int) -> int:
        if timestamp is None:
            timestamp = self._getCurrentTimestamp()
        cursor = self._connection.cursor()
        cursor = cursor.execute('INSERT INTO ' + self._tableRecords() + '(`timestamp`, deviceID, seconds) values(?, ?, ?)', (timestamp, deviceID, seconds))
        id = cursor.lastrowid
        self._connection.commit()
        return id

    def updateRecord(self, id: int, timestamp, deviceID: str, seconds: int) -> int:
        cursor = self._connection.cursor()
        if timestamp is not None:
            cursor = cursor.execute('UPDATE ' + self._tableRecords() + ' SET `timestamp`=? WHERE id = ?', (timestamp, id))
        if deviceID is not None:
            cursor = cursor.execute('UPDATE ' + self._tableRecords() + ' SET `deviceID`=? WHERE id = ?', (deviceID, id))
        if seconds is not None:
            cursor = cursor.execute('UPDATE ' + self._tableRecords() + ' SET `seconds`=? WHERE id = ?', (seconds, id))
        id = cursor.lastrowid
        self._connection.commit()
        return id

    def getRecords(self, fro: any = None, to: any = None) -> list:
        if fro is None:
            fro = self._getFirstTimestamp()
        if to is None:
            to = self._getCurrentTimestamp()
        cursor = self._connection.cursor()
        cursor = cursor.execute('SELECT id, `timestamp`, deviceID, seconds FROM ' + self._tableRecords() + ' WHERE `timestamp` >= ? and `timestamp` <= ?', (fro, to))
        devices = []
        for row in cursor.fetchall():
            devices.append(Record(id=row[0], timestamp=row[1], deviceID=row[2], seconds=row[3]))
        return devices

    def getRecordsByDevice(self, deviceID: str, fro: any = None, to: any = None) -> list:
        if fro is None:
            fro = self._getFirstTimestamp()
        if to is None:
            to = self._getCurrentTimestamp()
        cursor = self._connection.cursor()
        cursor = cursor.execute('SELECT id, `timestamp`, deviceID, seconds FROM ' + self._tableRecords() + ' WHERE `timestamp` >= ? and `timestamp` <= ? and deviceID=?', (fro, to, deviceID))
        devices = []
        for row in cursor.fetchall():
            devices.append(Record(id=row[0], timestamp=row[1], deviceID=row[2], seconds=row[3]))
        return devices
