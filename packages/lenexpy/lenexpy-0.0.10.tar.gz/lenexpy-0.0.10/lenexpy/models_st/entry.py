from datetime import time
from lenexpy.models.athelete import Athlete
from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper
from .swimtime import SwimTime


class Status(StrEnum):
    DNS = "DNS"
    DSQ = "DSQ"
    EXH = "EXH"
    RJC = "RJC"
    SICK = "SICK"
    WDR = "WDR"


class Entry(XmlRoot):
    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

    entrytime: SwimTime = XmlAttribute(name="entrytime")
    lane: int = XmlAttribute(name="lane")
    status: Status = XmlAttribute(name="status")
    clubname: str = XmlAttribute(name="clubname")
    athlete: Athlete = XmlElement(name='ATHLETE')
