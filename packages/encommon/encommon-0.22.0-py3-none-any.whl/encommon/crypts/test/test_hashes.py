"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..hashes import Hashes
from ...types import inrepr
from ...types import instr
from ...types import lattrs



def test_Hashes() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    hashes = Hashes('string')


    attrs = lattrs(hashes)

    assert attrs == [
        '_Hashes__string']


    assert inrepr(
        'hashes.Hashes object',
        hashes)

    assert isinstance(
        hash(hashes), int)

    assert instr(
        'hashes.Hashes object',
        hashes)


    assert hashes.string == 'string'

    assert hashes.md5[:3] == 'b45'
    assert hashes.md5[-2:] == '21'

    assert hashes.sha1[:3] == 'ecb'
    assert hashes.sha1[-2:] == '4d'

    assert hashes.sha256[:3] == '473'
    assert hashes.sha256[-2:] == 'a8'

    assert hashes.sha512[:3] == '275'
    assert hashes.sha512[-2:] == '87'

    assert hashes.uuid[:3] == '38f'
    assert hashes.uuid[-2:] == 'e4'

    assert hashes.apache[:3] == '7LJ'
    assert hashes.apache[-2:] == '0='
