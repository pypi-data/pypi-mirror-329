from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .relayposition import RelayPosition
from .club import Club


class StatusRelayPosition(StrEnum):
    DSQ = 'DSQ'
    DNF = 'DNF'


class RelayRecord(XmlRoot):
    club: Club = XmlElement(name="CLUB")
    name: str = XmlAttribute(name="name")
    relayPositions: List[RelayPosition] = XmlElementWrapper(
        "RELAYPOSITIONS", "RELAYPOSITION")
