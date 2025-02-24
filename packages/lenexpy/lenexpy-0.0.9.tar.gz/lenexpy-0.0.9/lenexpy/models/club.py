from lenexpy.strenum import StrEnum
from typing import TYPE_CHECKING, List, Optional, overload
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .nation import Nation
from .official import Official
from .relaymeet import RelayMeet
from .athelete import Athlete
from .contact import Contact


class TypeClub(StrEnum):
    CLUB = "CLUB",
    NATIONALTEAM = "NATIONALTEAM",
    REGIONALTEAM = "REGIONALTEAM",
    UNATTACHED = "UNATTACHED"


class Club(XmlRoot):
    if TYPE_CHECKING:
        @overload
        def __init__(
            self,
            name: str,
            shortname: Optional[str] = None,
            *,
            nation: Optional[str] = None,
            region: Optional[str] = None,
            contact: Optional[Contact] = None,
            athletes: Optional[List[Athlete]] = None,
            **kwargs
        ) -> None:
            pass

    def __init__(
        self,
        name: str,
        shortname: str = None,
        **kwargs
    ) -> None:
        self.name = name
        kwargs['shortname'] = shortname

        if 'contact' not in kwargs or kwargs['contact'].name is None:
            kwargs['contact'] = Contact(name=name)

        super().__init__(**kwargs)

    contact: Contact = XmlElement(name="CONTACT")
    code: str = XmlAttribute(name="code")
    athletes: List[Athlete] = XmlElementWrapper("ATHLETES", "ATHLETE")
    name: str = XmlAttribute(name="name", required=True)
    name_en: str = XmlAttribute(name="name.en")
    nation: Nation = XmlAttribute(name="nation")
    number: int = XmlAttribute(name="number")
    officials: List[Official] = XmlElementWrapper("OFFICIALS", "OFFICIAL")
    region: str = XmlAttribute(name="region")
    relays: List[RelayMeet] = XmlElementWrapper("RELAYS", "RELAY")
    shortname: str = XmlAttribute(name="shortname")
    shortname_en: str = XmlAttribute(name="shortname.en")
    swrid: str = XmlAttribute(name="swrid")
    type: TypeClub = XmlAttribute(name="type")
