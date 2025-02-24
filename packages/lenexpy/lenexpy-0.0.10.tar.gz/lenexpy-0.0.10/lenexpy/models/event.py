from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .fee import Fee
from .gender import Gender
from .heat import Heat
from .swimstyle import SwimStyle
from .timestandardref import TimeStandardRef
from .timing import Timing
from .agegroup import AgeGroup
from datetime import time as dtime


class Round(StrEnum):
    TIM = "TIM"
    FHT = "FHT"
    FIN = "FIN"
    SEM = "SEM"
    QUA = "QUA"
    PRE = "PRE"
    SOP = "SOP"
    SOS = "SOS"
    SOQ = "SOQ"


class TypeEvent(StrEnum):
    EMPTY = "EMPTY"
    MASTERS = "MASTERS"


class Event(XmlRoot):
    agegroups: List[AgeGroup] = XmlElementWrapper("AGEGROUPS", "AGEGROUP")
    daytime: dtime = XmlAttribute(name="daytime")
    eventid: int = XmlAttribute(name="eventid", required=True)
    fee: Fee = XmlElement(name="FEE")
    gender: Gender = XmlAttribute(name="gender")
    heats: List[Heat] = XmlElementWrapper("HEATS", 'HEAT')
    maxentries: int = XmlAttribute(name="maxentries")
    number: int = XmlAttribute(name="number", required=True)
    order: int = XmlAttribute(name="order")
    preveventid: int = XmlAttribute(name="preveventid")
    round: Round = XmlAttribute(name="round")
    run: int = XmlAttribute(name="run")
    swimstyle: SwimStyle = XmlElement(name="SWIMSTYLE", required=True)
    timeStandardRefs: List[TimeStandardRef] = XmlElementWrapper(
        "TIMESTANDARDREFS", "TIMESTANDARDREF")
    timing: Timing = XmlAttribute(name="timing")
    type: TypeEvent = XmlAttribute(name="type")
