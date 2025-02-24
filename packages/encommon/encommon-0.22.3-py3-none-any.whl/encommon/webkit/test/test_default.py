"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from pytest import fixture

from selenium.webdriver.remote.webdriver import WebDriver

from . import _executejs
from ...types.strings import SEMPTY

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



def test_default_create(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        '$("<p/>")[0]'
        '.tagName;')

    assert outcome == 'P'



def test_default_styles(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        '$("body>div")'
        '.css("color", "blue")'
        '.css("color", "red");',
        wrap=False)

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.style.color;')

    assert outcome == 'red'



def test_default_addClass(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        '$("body>div")'
        '.addClass("pytest")')

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.classList;')

    assert len(outcome) == 1



def test_default_remClass(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        '$("body>div")'
        '.remClass("pytest")')

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.classList;')

    assert len(outcome) == 0



def test_default_showhide(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.style.display;')

    assert outcome == SEMPTY

    _executejs(
        driver,
        '$("body>div").hide();',
        wrap=False)

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.style.display;')

    assert outcome == 'none'

    _executejs(
        driver,
        '$("body>div")'
        '.hide().show();',
        wrap=False)

    outcome = _executejs(
        driver,
        '$("body>div")[0]'
        '.style.display;')

    assert outcome == SEMPTY



def test_default_content(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare


    _executejs(
        driver,
        '$("body>div")'
        '.html("<p>pytest</p>");')

    outcome = _executejs(
        driver,
        '$("body>div").text();')

    assert outcome == 'pytest'


    _executejs(
        driver,
        '$("body>span")'
        '.text("pytest");')

    outcome = _executejs(
        driver,
        '$("body>span").text();')

    assert outcome == 'pytest'



def test_default_append(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        'let element = $("<p/>");'
        'let target = $("body");'
        'element.text("pytest");'
        'target.append(element);',
        wrap=False)

    outcome = _executejs(
        driver,
        '$("body>p")[0]'
        '.textContent;')

    assert outcome == 'pytest'



def test_default_replace(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        'let element = $("<p/>");'
        'let target = $("body");'
        'element.text("pytest");'
        'target.replace(element);',
        wrap=False)

    outcome = _executejs(
        driver,
        '$("body>p")[0]'
        '.textContent;')

    assert outcome == 'pytest'



def test_default_attr(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        '$("body")'
        '.attr("foo", "bar")')

    outcome = _executejs(
        driver,
        'return $("body")'
        ' .attr("foo");',
        wrap=False)

    assert outcome == 'bar'



def test_default_prop(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare

    _executejs(
        driver,
        '$("body")'
        '.prop("foo", "bar")')

    outcome = _executejs(
        driver,
        'return $("body")'
        ' .prop("foo");',
        wrap=False)

    assert outcome == 'bar'
