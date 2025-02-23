"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pytest import fixture
from pytest import mark
from pytest import raises

from ..crypts import Crypts
from ..params import CryptParams
from ..params import CryptsParams
from ...types import DictStrAny
from ...types import inrepr
from ...types import instr
from ...types import lattrs



@fixture
def crypts() -> Crypts:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    source: DictStrAny = {
        'default': {'phrase': Crypts.keygen()},
        'secrets': {'phrase': Crypts.keygen()}}

    params = CryptsParams(
        phrases=source)

    return Crypts(params)



def test_Crypts(
    crypts: Crypts,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param crypts: Primary class instance for the encryption.
    """


    attrs = lattrs(crypts)

    assert attrs == [
        '_Crypts__params']


    assert inrepr(
        'crypts.Crypts object',
        crypts)

    assert isinstance(
        hash(crypts), int)

    assert instr(
        'crypts.Crypts object',
        crypts)


    assert crypts.params

    assert len(crypts.keygen()) == 44



@mark.parametrize(
    'value,unique',
    [('foo', 'default'),
     ('foo', 'secrets')])
def test_Crypts_iterate(
    crypts: Crypts,
    value: str,
    unique: str,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param crypts: Primary class instance for the encryption.
    :param value: String value that will returned encrypted.
    :param unique: Unique identifier of mapping passphrase.
    """

    encrypt = (
        crypts.encrypt(value, unique))

    split = encrypt.split(';')

    assert split[1] == '1.0'
    assert split[2] == unique

    decrypt = crypts.decrypt(encrypt)

    assert decrypt == value



def test_Crypts_cover(
    crypts: Crypts,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param crypts: Primary class instance for the encryption.
    """


    crypts = Crypts()


    params = CryptParams(
        phrase=Crypts.keygen())

    crypts.create('testing', params)

    crypts.delete('testing')



def test_Crypts_raises(
    crypts: Crypts,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param crypts: Primary class instance for the encryption.
    """


    _raises = raises(ValueError)

    with _raises as reason:
        crypts.encrypt('foo', 'dne')

    _reason = str(reason.value)

    assert _reason == 'unique'


    _raises = raises(ValueError)

    with _raises as reason:
        crypts.decrypt('foo')

    _reason = str(reason.value)

    assert _reason == 'string'


    _raises = raises(ValueError)

    with _raises as reason:
        string = '$ENCRYPT;1.1;f;oo'
        crypts.decrypt(string)

    _reason = str(reason.value)

    assert _reason == 'version'


    _raises = raises(ValueError)

    params = CryptParams(phrase='foo')

    with _raises as reason:
        crypts.create('default', params)

    _reason = str(reason.value)

    assert _reason == 'unique'


    _raises = raises(ValueError)

    with _raises as reason:
        crypts.delete('dne')

    _reason = str(reason.value)

    assert _reason == 'unique'
