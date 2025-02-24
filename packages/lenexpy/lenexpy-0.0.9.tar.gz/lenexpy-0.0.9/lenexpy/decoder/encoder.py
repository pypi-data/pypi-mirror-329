from lenexpy.models.lenex import Lenex
from .lef_encoder import encode_lef
from .lxf_encoder import encode_lxf


def encode(lenex: Lenex, filename: str):
    if not filename.endswith(('.lxf', '.lef', '.xml')):
        raise TypeError('The file type must be .lxf, .lef, .xml')

    if filename.endswith(('.xml', '.lef')):
        return encode_lef(lenex, filename)
    if filename.endswith('.lxf'):
        return encode_lxf(lenex, filename)
