from pathlib import Path
import tempfile
from os.path import join
from zipfile import ZipFile, ZIP_DEFLATED
from lenexpy.models.lenex import Lenex
from .lef_encoder import encode_lef


def encode_lxf(lenex: Lenex, filename: str):
    if not filename.endswith('.lxf'):
        raise TypeError('The file type must be .lxf')

    fn = Path(filename).name[:-4] + '.lef'
    with tempfile.TemporaryDirectory() as dir:
        path = join(dir, fn)
        encode_lef(lenex, path)

        with ZipFile(
            filename,
            "w",
            compression=ZIP_DEFLATED
        ) as zf:
            zf.write(path, fn)
