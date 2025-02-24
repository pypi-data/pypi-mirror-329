from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper

from .ranking import Ranking
from .gender import Gender


class Calculate(StrEnum):
    TOTAL: str = 'TOTAL'
    SINGLE: str = 'SINGLE'


class AgeGroup(XmlRoot):
    id: int = XmlAttribute(name="agegroupid")
    agemax: int = XmlAttribute(required=True)
    agemin: int = XmlAttribute(required=True)
    gender: Gender = XmlAttribute()
    calculate: Calculate = XmlAttribute()
    handicap: int = XmlAttribute()
    levelmax: int = XmlAttribute()
    levelmin: int = XmlAttribute()
    levels: str = XmlAttribute()
    name: str = XmlAttribute()
    rankings: List[Ranking] = XmlElementWrapper('RANKINGS', 'RANKING')
