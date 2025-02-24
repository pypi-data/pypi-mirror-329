from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .agegroup import AgeGroup
from .course import Course
from .gender import Gender
from .timestandard import TimeStandard


class TypeTimeStandardList(StrEnum):
    DEFAULT = "DEFAULT"
    MAXIMUM = "MAXIMUM"
    MINIMUM = "MINIMUM"


class TimeStandardList(XmlRoot):
    id: int = XmlAttribute(name="timestandardlistid", required=True)
    age_group: AgeGroup = XmlElement(name="AGEGROUP")
    course: Course = XmlAttribute(name="course", required=True)
    gender: Gender = XmlAttribute(name="gender", required=True)
    handicap: int = XmlAttribute(name="handicap")
    name: str = XmlAttribute(name="name", required=True)
    timeStandards: List[TimeStandard] = XmlElementWrapper(
        "TIMESTANDARDS", "TIMESTANDARD", required=True)
    type: TypeTimeStandardList = XmlAttribute(name="type")
