from typing import TYPE_CHECKING, List, Literal, Optional, overload
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper
from datetime import date
from .entry import Entry
from .gender import Gender
from .handicap import Handicap
from .nation import Nation
from .result import Result


# required_params = {'birthday', 'gender', 'firstname', 'lastname'}/


class Athlete(XmlRoot):
    if TYPE_CHECKING:
        @overload
        def __init__(
            self,
            athleteid: int,
            *,
            birthdate: date,
            gender: Literal['F', 'M'],
            firstname: str,
            lastname: str,
            level: Optional[str] = None,
            **kwargs
        ):
            pass

    def __init__(self, id: int, **kwargs) -> None:
        self.athleteid = id
        super().__init__(**kwargs)

    athleteid: int = XmlAttribute(name="athleteid", required=True)
    birthdate: date = XmlAttribute(name="birthdate", required=True)
    entries: List[Entry] = XmlElementWrapper("ENTRIES", "ENTRY")
    firstname: str = XmlAttribute(name="firstname", required=True)
    firstname_en: str = XmlAttribute(name="firstname.en")
    gender: Gender = XmlAttribute(name="gender", required=True)
    handicap: Handicap = XmlElement(name="HANDICAP")
    lastname: str = XmlAttribute(name="lastname", required=True)
    lastname_en: str = XmlAttribute(name="lastname.en")
    level: str = XmlAttribute(name="level")
    license: str = XmlAttribute(name="license")
    nameprefix: str = XmlAttribute(name="nameprefix")
    nation: Nation = XmlAttribute(name="nation")
    passport: str = XmlAttribute(name="passport")
    results: List[Result] = XmlElementWrapper("RESULTS", "RESULT")
    swrid: int = XmlAttribute(name="swrid")
