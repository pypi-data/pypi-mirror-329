"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any

from pytest import fixture
from pytest import mark

from ..jinja2 import Jinja2
from ... import PROJECT
from ...times.common import UNIXMPOCH
from ...types import inrepr
from ...types import instr
from ...types import lattrs



@fixture
def jinja2() -> Jinja2:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """


    def strval(
        # NOCVR,
        input: str,
    ) -> str:
        return str(input)


    return Jinja2(
        {'PROJECT': PROJECT},
        {'strval': strval})



def test_Jinja2(
    jinja2: Jinja2,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param jinja2: Parsing class for the Jinja2 templating.
    """


    attrs = lattrs(jinja2)

    assert attrs == [
        '_Jinja2__statics',
        '_Jinja2__filters',
        '_Jinja2__jinjenv']


    assert inrepr(
        'jinja2.Jinja2 object',
        jinja2)

    assert isinstance(
        hash(jinja2), int)

    assert instr(
        'jinja2.Jinja2 object',
        jinja2)


    assert jinja2.statics

    assert jinja2.filters

    assert jinja2.jinjenv

    assert jinja2.parse('1') == 1



def test_Jinja2_recurse(
    jinja2: Jinja2,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param jinja2: Parsing class for the Jinja2 templating.
    """

    parse = jinja2.parse

    source = {
        'dict': {'key': '{{ "val" }}'},
        'list': [1, '{{ 2 }}', 3, '4'],
        'deep': '{{ {"foo": "bar"} }}'}

    parsed = parse(source)

    assert parsed == {
        'dict': {'key': 'val'},
        'list': [1, 2, 3, 4],
        'deep': {'foo': 'bar'}}

    _parsed = parse(f'{source}')

    assert _parsed == parsed



@mark.parametrize(
    'value,expect',
    [('{{ none }}', None),
     ('{{ 123 }}', 123),
     ('{{ 1.2 }}', 1.2),
     ('{{ -1.2 }}', -1.2)])
def test_Jinja2_literal(
    jinja2: Jinja2,
    value: Any,  # noqa: ANN401
    expect: Any,  # noqa: ANN401
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param jinja2: Parsing class for the Jinja2 templating.
    :param value: Input that will be processed and returned.
    :param expect: Expected output from the testing routine.
    """

    parse = jinja2.parse

    parsed = parse(value)

    parsed = parse(
        value,
        literal=False)

    assert parsed == str(expect)

    parsed = parse(
        value,
        literal=True)

    assert parsed == expect



@mark.parametrize(
    'value,expect',
    [('foo', 'foo'),
     ('1.0.0', '1.0.0'),
     ('1', 1),
     ('1.0', 1.0),
     ({'a': 'b'}, {'a': 'b'}),
     ("{'a': 'b'}", {'a': 'b'}),
     ('{{ 1 }}', 1),
     ('{{ "1" | float }}', 1.0),
     ('{{ "1" | int }}', 1),
     ('{{ 0 | Time }}', UNIXMPOCH),
     (100000, 100000),
     ('100000', 100000),
     (10.001, 10.001),
     ('10.001', 10.001),
     ([1, 2], [1, 2]),
     ('[1, 2]', [1, 2]),
     ('01', '01'),
     ('{{ "01" }}', '01'),
     ('-01', '-01'),
     ('{{ "-01" }}', '-01')])
def test_Jinja2_cover(
    jinja2: Jinja2,
    value: Any,  # noqa: ANN401
    expect: Any,  # noqa: ANN401
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param jinja2: Parsing class for the Jinja2 templating.
    :param value: Input that will be processed and returned.
    :param expect: Expected output from the testing routine.
    """

    parse = jinja2.parse

    parsed = parse(value)

    assert parsed == expect
