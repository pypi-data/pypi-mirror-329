import re
import lxml.etree as ET

from lenexpy.models.lenex import Lenex

BYTES_MODE = 'b'
ENCODING = 'utf-8'


def fix_declaration(text: str):
    def change(match: re.Match):
        return f'{match.group(1)}="{match.group(2)}"'

    return re.sub(r"([a-z]+)='([^']+)'",
                  change, text)


def get_declaration(text: str):
    return re.findall(r"<\?xml.*\?>", text)[0]


def change_declaration(text: str):
    declaration = get_declaration(text)
    declaration2 = fix_declaration(declaration)
    return text.replace(declaration, declaration2)


def encode_base(lenex: Lenex):
    xml_string: bytes = ET.tostring(
        lenex.dump('LENEX'),
        encoding=ENCODING,
        method="xml",
        xml_declaration=True
    )
    xml_string = change_declaration(xml_string.decode(ENCODING)).encode(ENCODING)
    return xml_string


def encode_lef(lenex: Lenex, filename: str):
    if not filename.endswith(('.lef', '.xml')):
        raise TypeError('The file type must be .lef, .xml')

    xml_string = encode_base(lenex)
    with open(filename, f"w{BYTES_MODE}+") as f:
        f.write(xml_string)
