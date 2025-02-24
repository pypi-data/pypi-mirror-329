from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute
from datetime import time as dtime


class Final(StrEnum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class StatusHeat(StrEnum):
    SEEDED = 'SEEDED'
    INOFFICIAL = 'INOFFICIAL'
    OFFICIAL = 'OFFICIAL'


class Heat(XmlRoot):
    agegroupid: int = XmlAttribute(name="agegroupid")
    daytime: dtime = XmlAttribute(name="daytime")
    finalType: Final = XmlAttribute(name="final")
    heatid: int = XmlAttribute(name="heatid", required=True)
    number: int = XmlAttribute(name="number", required=True)
    order: int = XmlAttribute(name="order")
    status: StatusHeat = XmlAttribute(name="status")
