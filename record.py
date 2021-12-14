from annotations import auto_str


@auto_str
class Record:

    def __init__(self, id: int, deviceID: str, seconds: int, timestamp) -> None:
        self.id = id
        self.deviceID = deviceID
        self.seconds = seconds
        self.timestamp = timestamp
