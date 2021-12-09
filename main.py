import json

from redis import utils
from actuator import Actuator
from device import Device
from configparser import ConfigParser
from cache.cachemanager import CacheManager
from cache.cachemanagerfactory import CacheManagerFactory
import utils
import logging

logging.basicConfig(
    format='%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
    level=logging.INFO,  # Nivel de los eventos que se registran en el logger
)
if __name__ == '__main__':
    parser = ConfigParser('config.yaml')
    config = parser.Load()
    if(not config):
        logging.error('No config provided')
        exit(1)
    if('devices' not in config or type(config['devices']) is not list):
        logging.error('No devices in config file')
        exit(1)
    if('cache-config' not in config or
       type(config['cache-config']) is not dict):
        logging.error('No cache-config in config file')
        exit(1)
    devicesdict = config['devices']
    devices = utils.DictToDevices(devicesdict)
    cacheManagerFactory = CacheManagerFactory(config['cache-config'])
    cacheManager = cacheManagerFactory.GetManager()
    cacheManager.PutSerializable('key', devices)
    print(cacheManager.GetSerializable('key'))
    print(utils.DictToDevices(cacheManager.GetSerializable('key')))
    print(utils.DevicesToDict(utils.DictToDevices(cacheManager.GetSerializable('key'))))
