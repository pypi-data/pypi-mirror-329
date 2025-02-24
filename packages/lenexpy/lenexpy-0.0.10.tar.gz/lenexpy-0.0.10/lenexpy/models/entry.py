from datetime import time
from lenexpy.strenum import StrEnum
from typing import List, Optional, Union
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .meetinfoentry import MeetInfoEntry
from .relayposition import RelayPosition
from .swimtime import SwimTime
from .course import Course


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
        eventid: int,
        entrytime: Optional[Union[str, time, SwimTime]] = None,
        **kwargs
    ):
        kwargs['eventid'] = eventid

        if isinstance(entrytime, (str, time)):
            entrytime = SwimTime._parse(entrytime)
        kwargs['entrytime'] = entrytime

        super().__init__(**kwargs)

    agegroupid: int = XmlAttribute(name="agegroupid")
    entrycourse: Course = XmlAttribute(name="entrycourse")
    entrytime: SwimTime = XmlAttribute(name="entrytime")
    eventid: int = XmlAttribute(name="eventid")
    heatid: int = XmlAttribute(name="heatid")
    lane: int = XmlAttribute(name="lane")
    meetinfo: MeetInfoEntry = XmlElement(name="MEETINFO")
    relay_positions: List[RelayPosition] = XmlElementWrapper(
        name="RELAYPOSITIONS")
    status: Status = XmlAttribute(name="status")
