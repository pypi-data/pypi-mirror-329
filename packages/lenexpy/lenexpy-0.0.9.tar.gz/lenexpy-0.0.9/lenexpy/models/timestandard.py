from xmlbind import XmlRoot, XmlAttribute, XmlElement

from .swimstyle import SwimStyle
from .swimtime import SwimTime


class TimeStandard(XmlRoot):
    swimstyle: SwimStyle = XmlElement(name="SWIMSTYLE", required=True)
    swimtime: SwimTime = XmlAttribute(name="swimtime", required=True)
