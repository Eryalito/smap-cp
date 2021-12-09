from abc import abstractmethod


class CacheManager():
    def __init__(self):
        pass

    @abstractmethod
    def PutValue(self, key: str, value: str) -> bool:
        pass

    @abstractmethod
    def GetValue(self, key: str) -> str:
        pass

    @abstractmethod
    def PutSerializable(self, key: str, value: any) -> bool:
        pass

    @abstractmethod
    def GetSerializable(self, key: str) -> any:
        pass
