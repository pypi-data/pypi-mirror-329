from xmlbind import XmlRoot, XmlAttribute, XmlElement

from .pool import Pool
from .swimtime import SwimTime
from .course import Course
from datetime import datetime, time as dtime


class MeetInfoEntry(XmlRoot):
    approved: str = XmlAttribute(name="approved")
    city: str = XmlAttribute(name="city")
    course: Course = XmlAttribute(name="course")
    date: datetime = XmlAttribute(name="date")
    daytime: dtime = XmlAttribute(name="daytime")
    name: str = XmlAttribute(name="name")
    nation: str = XmlAttribute(name="nation")
    pool: Pool = XmlElement(name="POOL")
    qualification_time: SwimTime = XmlAttribute(name="qualificationtime")
    state: str = XmlAttribute(name="state")
