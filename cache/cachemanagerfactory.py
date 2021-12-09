from cache.cachemanager import CacheManager
from cache.rediscachemanager import RedisCacheManager


class CacheManagerFactory:
    def __init__(self, cacheConfig: dict):
        self._config = cacheConfig

    def GetManager(self) -> CacheManager:
        type = self._config['type']
        if type == 'redis':
            return RedisCacheManager(
                host=self._config['host'] if 'host' in self._config
                else '127.0.0.1',
                port=int(self._config['port']) if 'port' in self._config
                else 6379,
                password=self._config['password'] if 'password' in self._config
                else None,
                errors=self._config['errors'] if 'errors' in self._config
                else 'strict',
                socket_timeout=float(self._config['socket_timeout'])
                if 'socket_timeout' in self._config else None,
                prefix=self._config['prefix'] if 'prefix' in self._config
                else '',
            )
        else:
            raise ValueError('Invalid cache-config type')
