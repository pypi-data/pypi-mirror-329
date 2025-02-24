from lenexpy.strenum import StrEnum
from xmlbind import XmlRoot, XmlAttribute, XmlElement

from .nation import Nation
from .contact import Contact
from .gender import Gender


class Official(XmlRoot):
    contact: Contact = XmlElement(name="CONTACT")
    firstname: str = XmlAttribute(name="firstname", required=True)
    gender: Gender = XmlAttribute(name="gender")
    grade: str = XmlAttribute(name="grade")
    lastname: str = XmlAttribute(name="lastname", required=True)
    license: str = XmlAttribute(name="license")
    nameprefix: str = XmlAttribute(name="nameprefix")
    nation: Nation = XmlAttribute(name="nation")
    officialid: int = XmlAttribute(name="officialid", required=True)
    passport: str = XmlAttribute(name="passport")
