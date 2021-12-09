from actuator import Actuator
from device import Device
from configparser import ConfigParser
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
    devicesdict = config['devices']
    devices = parser.ToDevices(devicesdict)
    print(devices[0])
    newDevice = Device('bff260753b1e87080d8cva',
                       '192.168.2.39', '8e850025ae7b977e', '3.3')
    deviceActuator = Actuator(newDevice)
    deviceActuator.TurnOn(10)
