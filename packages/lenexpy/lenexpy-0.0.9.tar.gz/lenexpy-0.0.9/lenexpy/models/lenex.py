from typing import List
from xmlbind import XmlRoot, XmlAttribute, XmlElement, XmlElementWrapper

from .meet import Meet
from .recordlist import RecordList
from .timestandardlist import TimeStandardList
from .constructor import Constructor


class Lenex(XmlRoot):
    constructor: Constructor = XmlElement(name="CONSTRUCTOR", required=True)
    meet: Meet = XmlElementWrapper("MEETS", 'MEET', with_list=False)
    recordLists: List[RecordList] = XmlElementWrapper("RECORDLISTS", "RECORDLIST")
    timeStandardLists: List[TimeStandardList] = XmlElementWrapper("TIMESTANDARDLISTS", "TIMESTANDARDLIST")
    version: str = XmlAttribute(name="version", required=True)
