import json
from cache.cachemanager import CacheManager
import redis


class RedisCacheManager(CacheManager):

    def __init__(self, host: str, port: int, password: str = None,
                 socket_timeout: float = None, errors: str = 'strict',
                 prefix: str = ''):
        super().__init__()
        self._prefix = prefix
        self._redis = redis.StrictRedis(
            host=host, port=port, password=password,
            socket_timeout=socket_timeout, errors=errors)

    def PutValue(self, key: str, value: str) -> bool:
        return self._redis.set(name=(self._prefix+key), value=value)

    def GetValue(self, key: str) -> str:
        return self._redis.get((self._prefix+key)).decode('utf-8')

    def PutSerializable(self, key: str, value: any) -> bool:
        return self._redis.set(name=(self._prefix+key),
                               value=self.CacheEncoder().encode(value))

    def GetSerializable(self, key: str) -> any:
        return json.loads(self._redis.get(self._prefix+key).decode('utf-8'))
