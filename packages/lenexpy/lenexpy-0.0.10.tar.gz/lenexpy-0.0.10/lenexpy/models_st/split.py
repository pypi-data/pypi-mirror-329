from xmlbind import XmlRoot, XmlAttribute

from .swimtime import SwimTime


class Split(XmlRoot):
    distance: int = XmlAttribute(name="distance", required=True)
    swimTime: SwimTime = XmlAttribute(name="swimtime", required=True)
