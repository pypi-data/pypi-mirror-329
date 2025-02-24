from typing import TYPE_CHECKING, Optional
from xmlbind import XmlRoot, XmlAttribute


class Contact(XmlRoot):
    if TYPE_CHECKING:
        def __init__(
            self,
            name: Optional[str] = None,
            city: Optional[str] = None,
            country: Optional[str] = None,
            email: Optional[str] = None,
            fax: Optional[str] = None,
            internet: Optional[str] = None,
            mobile: Optional[str] = None,
            phone: Optional[str] = None,
            state: Optional[str] = None,
            street: Optional[str] = None,
            street2: Optional[str] = None,
            zip: Optional[str] = None
        ):
            pass

    city: str = XmlAttribute(name="city")
    country: str = XmlAttribute(name="country")
    email: str = XmlAttribute(name="email")
    fax: str = XmlAttribute(name="fax")
    internet: str = XmlAttribute(name="internet")
    name: str = XmlAttribute(name="name")
    mobile: str = XmlAttribute(name="mobile")
    phone: str = XmlAttribute(name="phone")
    state: str = XmlAttribute(name="state")
    street: str = XmlAttribute(name="street")
    street2: str = XmlAttribute(name="street2")
    zip: str = XmlAttribute(name="zip")
