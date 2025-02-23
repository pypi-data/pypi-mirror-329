"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from re import compile
from re import match as re_match
from re import sub as re_sub
from typing import Optional
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet

from ..types.strings import SEMPTY

if TYPE_CHECKING:
    from .params import CryptParams
    from .params import CryptsParams



ENCRYPT = compile(
    r'^\$ENCRYPT;1\.\d;\S+\;.+?$')



class Crypts:
    """
    Encrypt and decrypt values using passphrase dictionary.

    .. testsetup::
       >>> from .params import CryptsParams

    Example
    -------
    >>> phrase = Crypts.keygen()
    >>> source = {'default': {'phrase': phrase}}
    >>> params = CryptsParams(phrases=source)
    >>> crypts = Crypts(params)
    >>> encrypt = crypts.encrypt('example')
    >>> encrypt
    '$ENCRYPT;1.0;default;...
    >>> crypts.decrypt(encrypt)
    'example'

    :param params: Parameters used to instantiate the class.
    """

    __params: 'CryptsParams'


    def __init__(
        self,
        params: Optional['CryptsParams'] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        from .params import (
            CryptsParams)

        if params is None:
            params = CryptsParams()

        self.__params = (
            deepcopy(params))


    @property
    def params(
        self,
    ) -> 'CryptsParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    def encrypt(
        self,
        value: str,
        unique: str = 'default',
    ) -> str:
        """
        Encrypt the provided value with the relevant passphrase.

        :param value: String value that will returned encrypted.
        :param unique: Unique identifier of mapping passphrase.
        :returns: Encrypted value using the relevant passphrase.
        """

        phrases = (
            self.params
            .phrases)

        if unique not in phrases:
            raise ValueError('unique')

        phrase = (
            phrases[unique]
            .phrase)

        encoded = value.encode()

        encrypt = (
            Fernet(phrase)
            .encrypt(encoded)
            .decode())

        return (
            '$ENCRYPT;1.0;'
            f'{unique};{encrypt}')


    def decrypt(
        self,
        value: str,
    ) -> str:
        """
        Decrypt the provided value with the relevant passphrase.

        :param value: String value that will returned decrypted.
        :returns: Decrypted value using the relevant passphrase.
        """

        phrases = (
            self.params
            .phrases)

        value = crypt_clean(value)

        match = re_match(
            ENCRYPT, value)

        if match is None:
            raise ValueError('string')

        version, unique, value = (
            value.split(';')[1:])

        if version != '1.0':
            raise ValueError('version')

        phrase = (
            phrases[unique]
            .phrase)

        encoded = value.encode()

        return (
            Fernet(phrase)
            .decrypt(encoded)
            .decode())


    def create(
        self,
        unique: str,
        params: 'CryptParams',
    ) -> None:
        """
        Create a new phrase using the provided input parameters.

        :param unique: Unique identifier of mapping passphrase.
        :param params: Parameters used to instantiate the class.
        """

        phrases = (
            self.params
            .phrases)

        if unique in phrases:
            raise ValueError('unique')

        phrases[unique] = params


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the phrase from the internal dictionary reference.

        :param unique: Unique identifier of mapping passphrase.
        """

        phrases = (
            self.params
            .phrases)

        if unique not in phrases:
            raise ValueError('unique')

        del phrases[unique]


    @classmethod
    def keygen(
        cls: object,
    ) -> str:
        """
        Return new randomly generated Fernet key for passphrase.

        :returns: Randomly generated Fernet key for passphrase.
        """

        key = Fernet.generate_key()

        return key.decode()



def crypt_clean(
    value: str,
) -> str:
    """
    Return the parsed and normalized encrypted string value.

    :param value: String value that will returned decrypted.
    :returns: Parsed and normalized encrypted string value.
    """

    return re_sub(r'[\n\s]', SEMPTY, value)
