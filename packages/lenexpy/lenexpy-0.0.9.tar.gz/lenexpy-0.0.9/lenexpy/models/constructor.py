from typing import Optional
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper
from .contact import Contact


class Constructor(XmlRoot):
    contact: Contact = XmlElement(required=False)
    name: str = XmlAttribute(required=True)
    registration: str = XmlAttribute()
    version: str = XmlAttribute(required=True)
