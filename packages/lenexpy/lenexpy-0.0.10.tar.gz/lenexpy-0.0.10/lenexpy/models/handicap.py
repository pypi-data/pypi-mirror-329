from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute


class HandicapClass(StrEnum):
    C1 = "1"
    C2 = "2"
    C3 = "3"
    C4 = "4"
    C5 = "5"
    C6 = "6"
    C7 = "7"
    C8 = "8"
    C9 = "9"
    C10 = "10"
    C11 = "11"
    C12 = "12"
    C13 = "13"
    C14 = "14"
    C15 = "15"
    GER_AB = "GER.AB"
    GER_GB = "GER.GB"


class Handicap(XmlRoot):
    breast: HandicapClass = XmlAttribute(name="breast", required=True)
    exception: str = XmlAttribute(name="exception")
    free: HandicapClass = XmlAttribute(name="free", required=True)
    medley: HandicapClass = XmlAttribute(name="medley", required=True)
