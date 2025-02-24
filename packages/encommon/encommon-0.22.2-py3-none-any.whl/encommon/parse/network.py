"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from typing import Any
from typing import Optional

from netaddr import IPAddress
from netaddr import IPNetwork



class Network:
    """
    Convert the network into the various supported formats.

    :param source: Network IPv4 or IPv6 network or address.
    """

    __source: IPNetwork


    def __init__(
        self,
        source: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        network = IPNetwork(source)

        self.__source = network


    def __repr__(
        self,
    ) -> str:
        """
        Built-in method for representing the values for instance.

        :returns: String representation for values from instance.
        """

        return f"Network('{self.address_cidr}')"


    def __hash__(
        self,
    ) -> int:
        """
        Built-in method called when performing hashing operation.

        :returns: Boolean indicating outcome from the operation.
        """

        return hash(self.__source)


    def __str__(
        self,
    ) -> str:
        """
        Built-in method for representing the values for instance.

        :returns: String representation for values from instance.
        """

        return self.address_cidr


    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        source = self.__source

        with suppress(Exception):

            other = IPNetwork(str(other))

            return source == other

        return False


    def __ne__(
        self,
        other: object,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        return not self.__eq__(other)


    @property
    def source(
        self,
    ) -> IPNetwork:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__source


    @property
    def version(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__source.version


    @property
    def cidr(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        return source.prefixlen


    @property
    def address(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        return str(source.ip)


    @property
    def address_cidr(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        address = self.address

        return f'{address}/{self.cidr}'


    @property
    def address_host(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        address = self.address

        prefix = (
            128
            if self.version == 6
            else 32)

        return f'{address}/{prefix}'


    @property
    def network(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        return str(source.network)


    @property
    def network_cidr(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        network = self.network

        return f'{network}/{self.cidr}'


    @property
    def broadcast(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        address = source.broadcast

        if address is None:
            return None

        return str(address)


    @property
    def padded(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.version != 4:
            raise ValueError('version')

        address = self.address

        octets = address.split('.')

        pads = [
            x.zfill(3)
            for x in octets]

        return '.'.join(pads)


    @property
    def reverse(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.version != 4:
            raise ValueError('version')


        address = self.address

        octets = address.split('.')

        reverse = list(reversed(octets))

        return '.'.join(reverse)


    @property
    def hwaddr(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.version != 4:
            raise ValueError('version')

        padded = self.padded

        nodots = (
            padded
            .replace('.', ''))

        ranged = range(
            0, len(nodots), 2)

        pairs = [
            nodots[x:x + 2]
            for x in ranged]

        return '-'.join(pairs)


    @property
    def netmask(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        return str(source.netmask)



    @property
    def ispublic(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether instance is state.
        """

        return (
            self.source.ip
            .is_global())


    @property
    def isprivate(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether instance is state.
        """

        return not self.ispublic


    @property
    def islinklocal(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether instance is state.
        """

        return (
            self.source
            .is_link_local())


    @property
    def islocalhost(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether instance is state.
        """

        return (
            self.source
            .is_loopback())



def insubnet_ip(
    address: str,
    networks: str | list[str] | tuple[str, ...],
) -> bool:
    """
    Return the boolean indicating address is in the network.

    :param address: Provided address to find in the network.
    :param network: Networks which values can be within any.
    :returns: Boolean indicating address is in the network.
    """

    if isinstance(networks, str):
        networks = [networks]

    networks = list(networks)

    if not isvalid_ip(address):
        raise ValueError('address')

    naddr = Network(address)

    if (naddr.version == 4
            and naddr.cidr == 32):
        address = naddr.address

    if (naddr.version == 6
            and naddr.cidr == 128):
        address = naddr.address

    parsed = IPAddress(address)

    return any(
        parsed in IPNetwork(x)
        for x in networks)



def isvalid_ip(
    value: Any,  # noqa: ANN401
) -> bool:
    """
    Return the boolean indicating whether the value is valid.

    :param value: Value that will be validated as an address.
    :returns: Boolean indicating whether the value is valid.
    """

    value = str(value)

    try:
        Network(value)
        return True

    except Exception:
        return False
