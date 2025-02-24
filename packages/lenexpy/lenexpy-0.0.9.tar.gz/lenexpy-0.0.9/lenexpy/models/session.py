from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .event import Event
from .fee import Fee
from .judge import Judge
from .pool import Pool
from .course import Course
from datetime import datetime, time as dtime


class Session(XmlRoot):
    course: Course = XmlAttribute(name="course")
    date: datetime = XmlAttribute(name="date", required=True)  # 2025-02-02
    daytime: dtime = XmlAttribute(name="daytime")
    events: List[Event] = XmlElementWrapper("EVENTS", "EVENT", required=True)
    fees: List[Fee] = XmlElementWrapper(name="FEES")
    judges: List[Judge] = XmlElementWrapper(name="JUDGES")
    name: str = XmlAttribute(name="name")
    number: int = XmlAttribute(name="number", required=True)
    officialmeeting: dtime = XmlAttribute(name="officialmeeting")
    pool: Pool = XmlElement(name="POOL")
    teamleadermeeting: dtime = XmlAttribute(name="teamleadermeeting")
    warmupfrom: dtime = XmlAttribute(name="warmupfrom")
    warmupuntil: dtime = XmlAttribute(name="warmupuntil")
