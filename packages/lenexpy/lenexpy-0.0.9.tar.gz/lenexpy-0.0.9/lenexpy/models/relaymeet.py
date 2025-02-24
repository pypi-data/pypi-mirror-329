from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .result import Result

from .entry import Entry
from .gender import Gender


class RelayMeet(XmlRoot):
    agemax: int = XmlAttribute(name="agemax", required=True)
    agemin: int = XmlAttribute(name="agemin", required=True)
    agetotalmax: int = XmlAttribute(name="agetotalmax", required=True)
    agetotalmin: int = XmlAttribute(name="agetotalmin", required=True)
    entries: List[Entry] = XmlElementWrapper("ENTRIES", "ENTRY")
    gender: Gender = XmlAttribute(name="gender", required=True)
    handicap: int = XmlAttribute(name="handicap")
    name: str = XmlAttribute(name="name")
    number: int = XmlAttribute(name="number")
    results: List[Result] = XmlElementWrapper("RESULTS", "RESULT")
