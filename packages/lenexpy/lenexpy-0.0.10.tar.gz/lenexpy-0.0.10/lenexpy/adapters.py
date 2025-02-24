from datetime import datetime, date, time as dtime
from xmlbind.compiler import XmlCompiler
from xmlbind.settings import add_compiler

from .models.swimtime import SwimTime, SwimTimeAttr


class DTimeCompiler(XmlCompiler[dtime]):
    def __init__(self):
        super().__init__(dtime)

    def unmarshal(self, v):
        if not v:
            return None
        return dtime.fromisoformat(v)

    def marshal(self, v):
        if not v:
            return None
        return dtime.isoformat(v)


class DateCompiler(XmlCompiler[date]):
    def __init__(self):
        super().__init__(date)

    def unmarshal(self, v):
        if not v:
            return None
        return date.fromisoformat(v)

    def marshal(self, v):
        if not v:
            return None
        return date.isoformat(v)


class DtCompiler(XmlCompiler[datetime]):
    def __init__(self):
        super().__init__(datetime)

    def unmarshal(self, v):
        if not v:
            return None
        return datetime.fromisoformat(v)

    def marshal(self, v):
        if not v:
            return None
        return datetime.isoformat(v)


class IntCompiler(XmlCompiler[int]):
    def __init__(self):
        super().__init__(int)

    def unmarshal(self, v):
        if not v:
            return None
        return int(v)

    def marshal(self, v):
        if not v:
            return None
        return str(v)


class SwimTimeCompiler(XmlCompiler[SwimTime]):
    def __init__(self):
        super().__init__(SwimTime)

    def unmarshal(self, v):
        if not v:
            return SwimTime.from_attrib(SwimTimeAttr.NT)
        return SwimTime._parse(v)

    def marshal(self, v: SwimTime):
        return str(v)


add_compiler(DateCompiler())
add_compiler(DTimeCompiler())
add_compiler(DtCompiler())
add_compiler(IntCompiler())
add_compiler(SwimTimeCompiler())


if __name__ == '__main__':
    comp = SwimTimeCompiler()
    print(comp.unmarshal('NT'))
    d = comp.unmarshal('00:00:19.35')
    print(d)

    comp = DateCompiler()
    print(comp.unmarshal('24.12.2008'))
