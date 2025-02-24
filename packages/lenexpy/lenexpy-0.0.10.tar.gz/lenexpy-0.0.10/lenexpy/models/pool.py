from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElement


class TypePool(StrEnum):
    INDOOR = "INDOOR"
    OUTDOOR = "OUTDOOR"
    LAKE = "LAKE"
    OCEAN = "OCEAN"


class Pool(XmlRoot):
    name: str = XmlAttribute(name="name")
    lanemax: int = XmlAttribute(name="lanemax")
    lanemin: int = XmlAttribute(name="lanemin")
    temperature: int = XmlAttribute(name="temperature")
    type: TypePool = XmlAttribute(name="type")
