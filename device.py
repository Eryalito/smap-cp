from annotations import auto_str


@auto_str
class Device:
    def __init__(self, identifier: str, ip: str,
                 key: str, version: str, name: str = ''):
        self.id = identifier
        self.ip = ip
        self.key = key
        self.version = version
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
