from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElement

from .reactiontime import ReactionTime
from .meetinfoentry import MeetInfoEntry


class StatusRelayPosition(StrEnum):
    DSQ = 'DSQ'
    DNF = 'DNF'


class RelayPosition(XmlRoot):
    athleteid: int = XmlAttribute(name="athleteid")
    meetinfo: MeetInfoEntry = XmlElement(name="MEETINFO")
    number: int = XmlAttribute(name="number", required=True)
    reaction_time: ReactionTime = XmlAttribute(name="reactiontime")
    status: StatusRelayPosition = XmlAttribute(name="status")
