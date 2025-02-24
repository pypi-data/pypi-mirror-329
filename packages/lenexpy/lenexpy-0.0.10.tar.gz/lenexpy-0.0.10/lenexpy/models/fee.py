from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute
from .currency import Currency


class TypeFee(StrEnum):
    CLUB = "CLUB"
    ATHLETE = "ATHLETE"
    RELAY = "RELAY"
    TEAM = "TEAM"
    LATEENTRY_INDIVIDUAL = "LATEENTRY.INDIVIDUAL"
    LATEENTRY_RELAY = "LATEENTRY.RELAY"


class Fee(XmlRoot):
    currency: Currency = XmlAttribute(name="currency", required=True)
    type: TypeFee = XmlAttribute(name="type")
    value: int = XmlAttribute("value", required=True)
