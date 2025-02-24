from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute
from .stroke import Stroke


class Technique(StrEnum):
    DIVE = "DIVE"
    GLIDE = "GLIDE"
    KICK = "KICK"
    PULL = "PULL"
    START = "START"
    TURN = "TURN"


class SwimStyle(XmlRoot):
    code: str = XmlAttribute(name="code")
    distance: int = XmlAttribute(name="distance", required=True)
    name: str = XmlAttribute(name="name")
    relaycount: int = XmlAttribute(name="relaycount", required=True)
    stroke: Stroke = XmlAttribute(name="stroke", required=True)
    swimstyleid: int = XmlAttribute(name="swimstyleid")
    technique: Technique = XmlAttribute(name="technique")
