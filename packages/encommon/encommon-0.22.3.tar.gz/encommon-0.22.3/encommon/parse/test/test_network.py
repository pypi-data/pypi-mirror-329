"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pytest import raises

from ..network import Network
from ..network import insubnet_ip
from ..network import isvalid_ip
from ...types import inrepr
from ...types import instr
from ...types import lattrs



def test_Network() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    naddr = Network('12.34.56.7')


    attrs = lattrs(naddr)

    assert attrs == [
        '_Network__source']


    assert inrepr(
        "Network('12.34.",
        naddr)

    assert isinstance(
        hash(naddr), int)

    assert instr(
        '12.34.56.7/32',
        naddr)


    assert naddr == '12.34.56.7'
    assert naddr != 'invalid'


    assert naddr.source

    assert naddr.version == 4

    assert naddr.cidr == 32

    assert naddr.address == '12.34.56.7'

    assert naddr.address_cidr == '12.34.56.7/32'

    assert naddr.address_host == '12.34.56.7/32'

    assert naddr.network == '12.34.56.7'

    assert naddr.network_cidr == '12.34.56.7/32'

    assert not naddr.broadcast

    assert naddr.netmask == '255.255.255.255'

    assert naddr.padded == '012.034.056.007'

    assert naddr.reverse == '7.56.34.12'

    assert naddr.hwaddr == '01-20-34-05-60-07'

    assert naddr.ispublic

    assert not naddr.isprivate

    assert not naddr.islinklocal

    assert not naddr.islocalhost



def test_Network_ipv4() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    naddr = Network('12.34.56.7/24')


    assert naddr.cidr == 24

    assert naddr.address == '12.34.56.7'

    assert naddr.address_cidr == '12.34.56.7/24'

    assert naddr.address_host == '12.34.56.7/32'

    assert naddr.network == '12.34.56.0'

    assert naddr.network_cidr == '12.34.56.0/24'

    assert naddr.broadcast == '12.34.56.255'

    assert naddr.netmask == '255.255.255.0'

    assert naddr.padded == '012.034.056.007'

    assert naddr.reverse == '7.56.34.12'

    assert naddr.hwaddr == '01-20-34-05-60-07'

    assert naddr.ispublic

    assert not naddr.isprivate

    assert not naddr.islinklocal

    assert not naddr.islocalhost



def test_Network_ipv6() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    naddr = Network('2001:db8::/64')


    assert naddr.cidr == 64

    assert naddr.address == '2001:db8::'

    assert naddr.address_cidr == '2001:db8::/64'

    assert naddr.address_host == '2001:db8::/128'

    assert naddr.network == '2001:db8::'

    assert naddr.network_cidr == '2001:db8::/64'

    assert naddr.broadcast == (
        '2001:db8::ffff:ffff:ffff:ffff')

    assert naddr.netmask == (
        'ffff:ffff:ffff:ffff::')

    with raises(ValueError):
        naddr.padded

    with raises(ValueError):
        naddr.reverse

    with raises(ValueError):
        naddr.hwaddr

    assert not naddr.ispublic

    assert naddr.isprivate

    assert not naddr.islinklocal

    assert not naddr.islocalhost



def test_isvalid_ip() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert isvalid_ip('1.2.3.4')

    assert not isvalid_ip('1.2')

    assert not isvalid_ip(None)



def test_insubnet_ip() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert insubnet_ip(
        '192.168.1.1',
        ['172.16.0.0/12',
         '192.168.0.0/16'])

    assert not insubnet_ip(
        '1.2.3.4',
        ['172.16.0.0/12',
         '192.168.0.0/16'])

    assert insubnet_ip(
        '192.168.1.1',
        ['192.168.1.1/32'])

    assert insubnet_ip(
        '192.168.1.1/32',
        '192.168.1.1/32')

    assert insubnet_ip(
        '2001:db8::',
        ['2001:db8::/128'])

    assert insubnet_ip(
        '2001:db8::',
        ['2001:db8::/32'])

    assert insubnet_ip(
        '2001:db8::/128',
        ['2001:db8::/32'])

    with raises(ValueError):

        insubnet_ip(
            'invalid',
            ['2001:db8::/32'])
