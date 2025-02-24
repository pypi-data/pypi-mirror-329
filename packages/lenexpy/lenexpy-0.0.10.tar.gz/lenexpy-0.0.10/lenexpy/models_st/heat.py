from typing import List
from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper
from datetime import time as dtime
from .entry import Entry
from .result import Result


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
    heatid: int = XmlAttribute(name="heatid", required=True)
    daytime: dtime = XmlAttribute(name="daytime")
    name: str = XmlAttribute(name="name")
    number: int = XmlAttribute(name="number")
    order: int = XmlAttribute(name="order")
    status: StatusHeat = XmlAttribute(name="status")
    entries: List[Entry] = XmlElementWrapper("ENTRIES", "ENTRY")
    reesults: List[Result] = XmlElementWrapper("RESULTS", "RESULT")
