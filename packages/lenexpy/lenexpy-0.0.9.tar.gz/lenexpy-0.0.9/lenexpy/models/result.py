from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper

from .split import Split
from .swimtime import SwimTime

from .relayposition import RelayPosition
from .reactiontime import ReactionTime


class StatusResult(StrEnum):
    EXH = "EXH"
    DSQ = "DSQ"
    DNS = "DNS"
    DNF = "DNF"
    SICK = "SICK"
    WDR = "WDR"


class Result(XmlRoot):
    comment: str = XmlAttribute(name="comment")
    eventid: int = XmlAttribute(name="eventid", required=True)
    heatid: int = XmlAttribute(name="heatid")
    lane: int = XmlAttribute(name="lane")
    points: int = XmlAttribute(name="points")
    reactionTime: ReactionTime = XmlAttribute(name="reactiontime")
    relayPositions: List[RelayPosition] = XmlElementWrapper(
        name="RELAYPOSITIONS")
    resultid: int = XmlAttribute(name="resultid", required=True)
    status: StatusResult = XmlAttribute(name="status")
    splits: List[Split] = XmlElementWrapper(name="SPLITS")
    swimTime: SwimTime = XmlAttribute(name="swimtime")
