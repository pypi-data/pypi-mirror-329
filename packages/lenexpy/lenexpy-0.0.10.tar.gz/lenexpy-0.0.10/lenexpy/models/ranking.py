from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElement


class Ranking(XmlRoot):
    order: int = XmlAttribute(name="order")
    place: int = XmlAttribute(name="place", required=True)
    result_id: int = XmlAttribute(name="resultid", required=True)
