from io import BytesIO
import re
import lxml.etree as ET
from zipfile import ZipFile
from lenexpy.models.lenex import Lenex


def decode_lxf(filename: str) -> Lenex:
    with open(filename, 'rb') as file:
        return decode_lxf_bytes(BytesIO(file.read()))


def decode_lxf_bytes(data: BytesIO) -> Lenex:
    with ZipFile(data) as zp:
        if len(zp.filelist) != 1:
            raise TypeError("Incorrect lenex file")
        with zp.open(zp.filelist[0]) as file:
            data = file.read()

    element = ET.fromstring(data)
    return Lenex._parse(element)
