from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .meetinforecord import MeetInfoRecord
from .relayrecord import RelayRecord
from .split import Split
from .swimstyle import SwimStyle
from .swimtime import SwimTime
from .athelete import Athlete


class Record(XmlRoot):
    athlete: Athlete = XmlElement(name="ATHLETE")
    comment: str = XmlAttribute(name="comment")
    meetInfo: MeetInfoRecord = XmlElement(name="MEETINFO")
    relay: RelayRecord = XmlElement(name="RELAY")
    splits: List[Split] = XmlElementWrapper("SPLITS", "SPLIT")
    swimstyle: SwimStyle = XmlElement(name="SWIMSTYLE", required=True)
    swimtime: SwimTime = XmlAttribute(name="swimtime", required=True)
    status: str = XmlAttribute(name="status")
