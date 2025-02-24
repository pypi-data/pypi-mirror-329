from datetime import datetime, time as dtime, date
from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .agedate import AgeDate
from .nation import Nation
from .pointtable import PointTable
from .pool import Pool
from .qualify import Qualify
from .session import Session
from .timing import Timing
from .course import Course
from .contact import Contact
from .club import Club
from .fee import Fee


class EntryType(StrEnum):
    OPEN = 'OPEN'
    INVITATION = 'INVITATION'


class Meet(XmlRoot):
    agedate: AgeDate = XmlElement(name="AGEDATE")
    altitude: int = XmlAttribute(name="altitude")
    city: str = XmlAttribute(name="city", required=True)
    city_en: str = XmlAttribute(name="city.en")
    clubs: List[Club] = XmlElementWrapper("CLUBS", 'CLUB')
    contact: Contact = XmlElement(name="CONTACT")
    course: Course = XmlAttribute(name="course")
    deadline: date = XmlAttribute(name="deadline")
    deadline_time: dtime = XmlAttribute(name="deadlinetime")
    entry_start_date: date = XmlAttribute(name="entrystartdate")
    entry_type: EntryType = XmlAttribute(name="entrytype")
    fees: List[Fee] = XmlElement(name="FEE")
    host_club: str = XmlAttribute(name="hostclub")
    host_club_url: str = XmlAttribute(name="hostclub.url")
    max_entries: int = XmlAttribute(name="maxentries")
    name: str = XmlAttribute(name="name", required=True)
    name_en: str = XmlAttribute(name="name.en")
    nation: Nation = XmlAttribute(name="nation", required=True)
    number: str = XmlAttribute(name="number")
    organizer: str = XmlAttribute(name="organizer")
    organizer_url: str = XmlAttribute(name="organizer.url")
    point_table: PointTable = XmlElement(name="POINTTABLE")
    pool: Pool = XmlElement(name="POOL")
    qualify: Qualify = XmlElement(name="QUALIFY")
    result_url: str = XmlAttribute(name="result.url")
    sessions: List[Session] = XmlElementWrapper(
        "SESSIONS", 'SESSION', required=True)
    state: str = XmlAttribute(name="state")
    uid: str = XmlAttribute(name="swrid")
    timing: Timing = XmlAttribute(name="timing")
    type: str = XmlAttribute(name="type")
