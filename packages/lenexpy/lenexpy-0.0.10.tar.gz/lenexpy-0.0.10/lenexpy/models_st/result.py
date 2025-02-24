from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper

from .split import Split
from .swimtime import SwimTime
from .reactiontime import ReactionTime


class StatusResult(StrEnum):
    EXH = "EXH"
    DSQ = "DSQ"
    DNS = "DNS"
    DNF = "DNF"
    SICK = "SICK"
    WDR = "WDR"


class Result(XmlRoot):
    lane: int = XmlAttribute(name="lane", required=True)
    swim_time: SwimTime = XmlAttribute(name="swimtime", required=True)
    status: StatusResult = XmlAttribute(name="status")
    reaction_time: ReactionTime = XmlAttribute(name="reactiontime")
    splits: List[Split] = XmlElementWrapper("SPLITS", "SPLIT")
