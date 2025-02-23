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
        {content.scripts('numeric')}
            </script>
          </head>
          <body>
            <div>Hello</div>
            <span>World</span>
          </body>
        </html>
        """)

    return (content, driver)



def test_numeric(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare


    outcome = _executejs(
        driver,
        'let element ='
        ' numeric(...arguments);'
        'return'
        ' element[0].outerHTML;',
        1.1, 'gb',
        wrap=False)

    assert outcome == (
        '<div class="encommon_numeric">'
        '<span class="_value">1</span>'
        '<span class="_delim">.</span>'
        '<span class="_decimal">1</span>'
        '<span class="_unit">gb</span>'
        '</div>')


    outcome = _executejs(
        driver,
        'let element ='
        ' numeric(...arguments);'
        'return'
        ' element[0].outerHTML;',
        1.0, 'gb',
        wrap=False)

    assert outcome == (
        '<div class="encommon_numeric">'
        '<span class="_value">1</span>'
        '<span class="_unit">gb</span>'
        '</div>')



def test_numeric_count(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare


    outcome = _executejs(
        driver,
        'let element ='
        ' numeric_count(...arguments);'
        'return'
        ' element[0].outerHTML;',
        1e10 + 1e8,
        wrap=False)


    assert outcome == (
        '<div class="encommon_numeric">'
        '<span class="_value">10</span>'
        '<span class="_delim">.</span>'
        '<span class="_decimal">1</span>'
        '<span class="_unit">billion</span>'
        '</div>')



def test_numeric_bytes(
    prepare: tuple['Content', WebDriver],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param prepare: Driver and content loaded with scripts.
    """

    content, driver = prepare


    outcome = _executejs(
        driver,
        'let element ='
        ' numeric_bytes(...arguments);'
        'return'
        ' element[0].outerHTML;',
        1e10 + 1e8,
        wrap=False)


    assert outcome == (
        '<div class="encommon_numeric">'
        '<span class="_value">10</span>'
        '<span class="_delim">.</span>'
        '<span class="_decimal">1</span>'
        '<span class="_unit">GB</span>'
        '</div>')
