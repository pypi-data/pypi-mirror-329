
from lenexpy.decoder.lef_decoder import decode_lef
from lenexpy.decoder.lxf_decoder import decode_lxf
from lenexpy.models.lenex import Lenex


def decode(filename: str) -> Lenex:
    if filename.endswith(('.xml', '.lef')):
        return decode_lef(filename)
    if filename.endswith('.lxf'):
        return decode_lxf(filename)
