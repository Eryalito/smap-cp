from database.smapdb import SMAPDB
from database.smapdbsqlite import SMAPDBSQLite


class SMAPDBFactory():

    def __init__(self, dbConfig: dict):
        self._config = dbConfig

    def getDB(self) -> SMAPDB:
        type = self._config['type']
        if type == 'sqlite':
            return SMAPDBSQLite(
                file=self._config['file'] if 'file' in self._config
                else 'database.db',
                prefix=self._config['prefix'] if 'prefix' in self._config
                else '',
            )
        else:
            raise ValueError('Invalid database-config type')
