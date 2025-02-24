from typing import TYPE_CHECKING, List, Literal, Optional, overload
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper
from datetime import date
from .handicap import Handicap
from .nation import Nation


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
    firstname: str = XmlAttribute(name="firstname", required=True)
    lastname: str = XmlAttribute(name="lastname", required=True)
    handicap: Handicap = XmlElement(name="HANDICAP")
    nation: Nation = XmlAttribute(name="nation")
