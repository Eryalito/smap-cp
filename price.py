from annotations import auto_str


@auto_str
class Price:
    def __init__(self, day: str, start: str, length: str, price: float) -> None:
        self.day = day
        self.start = start
        self.length = length
        self.price = price
