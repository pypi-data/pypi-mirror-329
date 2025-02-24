from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper
from .gender import Gender
from .agegroup import AgeGroup
from .course import Course
from .record import Record
from datetime import datetime, time as dtime


class RecordList(XmlRoot):
    ageGroup: AgeGroup = XmlElement(name="AGEGROUP")
    course: Course = XmlAttribute(name="course", required=True)
    gender: Gender = XmlAttribute(name="gender", required=True)
    handicap: int = XmlAttribute(name="handicap")
    name: str = XmlAttribute(name="name", required=True)
    nation: str = XmlAttribute(name="nation")
    order: int = XmlAttribute(name="order")
    records: List[Record] = XmlElementWrapper(
        "RECORDS",  "RECORD", required=True)
    region: str = XmlAttribute(name="region")
    updated: datetime = XmlAttribute(name="updated")
    type: str = XmlAttribute(name="type")
