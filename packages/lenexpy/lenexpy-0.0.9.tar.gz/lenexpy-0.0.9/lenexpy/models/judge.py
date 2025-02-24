from lenexpy.strenum import StrEnum
from typing import List
from xmlbind import XmlRoot, XmlAttribute


class Role(StrEnum):
    OTH = "OTH"
    MDR = "MDR"
    TDG = "TDG"
    REF = "REF"
    STA = "STA"
    ANN = "ANN"
    JOS = "JOS"
    CTIK = "CTIK"
    TIK = "TIK"
    CFIN = "CFIN"
    FIN = "FIN"
    CIOT = "CIOT"
    IOT = "IOT"
    FSR = "FSR"
    COC = "COC"
    CREC = "CREC"
    REC = "REC"
    CRS = "CRS"
    CR = "CR"
    MED = "MED"


class Judge(XmlRoot):
    number: int = XmlAttribute(name="number")
    officialid: int = XmlAttribute(name="officialid", required=True)
    role: Role = XmlAttribute(name="role")
