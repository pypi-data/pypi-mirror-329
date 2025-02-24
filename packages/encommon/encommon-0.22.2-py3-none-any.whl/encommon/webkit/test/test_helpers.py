"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from pytest import fixture

from selenium.webdriver.remote.webdriver import WebDriver

from . import _executejs

if TYPE_CHECKING:
    from ..content import Content



@fixture
def prepare(
    content: 'Content',
    driver: WebDriver,
) -> tuple['Content', WebDriver]:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    driver.get(
        f"""
        data:text/html;
        charset=utf-8,
        <html>
          <head>
            <script>
        {content.scripts('default')}
        {content.scripts('helpers')}
            </script>
          </head>
          <body>
            <div>Hello</div>
            <span>World</span>
          </body>
        </html>
        """)

    return (content, driver)



def test_helpers_assert(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'assert(1 == 1)')

    assert outcome is True



def test_helpers_whenready(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        'whenready('
        'console.log)')



def test_helpers_isnull(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isnull(undefined)'
        ' && isnull(null)')

    assert outcome is True



def test_helpers_isempty(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isempty({})'
        ' && isempty("")'
        ' && isempty([])')

    assert outcome is True



def test_helpers_isbool(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isbool(true)')

    assert outcome is True



def test_helpers_isstr(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isstr("string")')

    assert outcome is True

    outcome = _executejs(
        driver,
        'isstr(69429)')

    assert outcome is False



def test_helpers_isnum(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isnum(123)')

    assert outcome is True

    outcome = _executejs(
        driver,
        'isnum(1.23)')

    assert outcome is True

    outcome = _executejs(
        driver,
        'isnum("69429")')

    assert outcome is False



def test_helpers_isquery(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        ('let element = $("<p/>");'
         'return isquery(element);'),
        wrap=False)

    assert outcome is True



def test_helpers_isnode(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        ('let element = $("<p/>");'
         'return isnode(element[0]);'),
        wrap=False)

    assert outcome is True



def test_helpers_istime(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'istime("2024-04-20")')

    assert outcome is True



def test_helpers_islist(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'islist([69429])')

    assert outcome is True



def test_helpers_isdict(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isdict({"foo": "bar"})')

    assert outcome is True



def test_helpers_istrue(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'istrue(true)')

    assert outcome is True



def test_helpers_isfalse(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'isfalse(false)')

    assert outcome is True



def test_helpers_loads(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        'loads(\'{"foo":"bar"}\')')

    assert outcome['foo'] == 'bar'



def test_helpers_dumps(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    dumped = '{"foo":"bar"}'

    outcome = _executejs(
        driver,
        'dumps({"foo": "bar"})')

    assert outcome == dumped
