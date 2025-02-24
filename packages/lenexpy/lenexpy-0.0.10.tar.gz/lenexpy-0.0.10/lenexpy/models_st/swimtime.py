from datetime import time
from lenexpy.strenum import StrEnum
from typing import TYPE_CHECKING, Union


class SwimTimeAttr(StrEnum):
    # NT - Not Time or
    NT = 'NT'


class SwimTime:
    if TYPE_CHECKING:
        NT: 'SwimTime'

    def __init__(self, hour: int, minute: int, second: int, hsec: int):
        self.attrib = None
        self.hour = hour
        self.minute = minute
        self.second = second
        self.hsec = hsec

    @classmethod
    def from_attrib(cls, attrib: SwimTimeAttr) -> 'SwimTime':
        self = cls(0, 0, 0, 0)
        self.attrib = attrib
        return self

    @classmethod
    def _parse(cls, t: Union[time, str]):
        if isinstance(t, str):
            t = t.strip()
            if t == SwimTimeAttr.NT:
                return cls.from_attrib(t)
            t = time.fromisoformat(t)
        return cls(t.hour, t.minute, t.second, t.microsecond // 10000)

    def __str__(self):
        if self.attrib is not None:
            return self.attrib
        return "%02d:%02d:%02d.%02d" % (self.hour, self.minute, self.second, self.hsec)

    def as_duration(self):
        return self.hour*60*60 + self.minute*60 + self.second + self.hsec / 100


SwimTime.NT = SwimTime.from_attrib(SwimTimeAttr.NT)
