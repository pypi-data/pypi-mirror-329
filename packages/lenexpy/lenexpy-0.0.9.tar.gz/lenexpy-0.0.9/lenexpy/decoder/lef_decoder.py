import lxml.etree as ET
from lenexpy.models.lenex import Lenex


def decode_lef(filename: str) -> Lenex:
    with open(filename, 'rb') as file:
        element = ET.fromstring(file.read())
    return Lenex._parse(element)


def decode_lef_bytes(data: bytes) -> Lenex:
    return Lenex._parse(ET.fromstring(data))
