from annotations import auto_str


@auto_str
class Price:
    def __init__(self, day: str, hour: str, price: float) -> None:
        self.day = day
        self.hour = hour
        self.price = price
