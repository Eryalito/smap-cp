from annotations import auto_str


@auto_str
class Step:
    def __init__(self, days: str, start: int, end: int, count: int):
        self.days = days
        self.start = start
        self.end = end
        self.count = count

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, value):
        self._days = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
