import yaml
from yaml.loader import Loader
from device import Device


class ConfigParser:
    def __init__(self, path: str):
        self._path = path

    def Load(self) -> dict:
        a_yaml_file = open(self._path)
        return yaml.load(a_yaml_file, Loader=yaml.FullLoader)
