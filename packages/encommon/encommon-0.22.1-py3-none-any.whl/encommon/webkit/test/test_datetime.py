"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from selenium.webdriver.remote.webdriver import WebDriver

from . import _executejs

if TYPE_CHECKING:
    from ..content import Content



def test_datestamp(
    content: 'Content',
    driver: WebDriver,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param content: Primary class instance for the content.
    :param driver: Selenium driver provided by the library.
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
        {content.scripts('datetime')}
            </script>
          </head>
          <body></body>
        </html>
        """)


    outcome = _executejs(
        driver,
        'let element ='
        ' datestamp(...arguments);'
        'return'
        ' element[0].outerHTML;',
        '2024-04-20T16:20:00Z',
        wrap=False)


    assert outcome == (
        '<div class="encommon_datestamp">'
        '<span class="_value _year">2024</span>'
        '<span class="_delim _slash">-</span>'
        '<span class="_value _month">04</span>'
        '<span class="_delim _slash">-</span>'
        '<span class="_value _day">20</span>'
        '<span class="_delim _space">&nbsp;</span>'
        '<span class="_value _hours">16</span>'
        '<span class="_delim _colon">:</span>'
        '<span class="_value _minutes">20</span>'
        '<span class="_delim _colon">:</span>'
        '<span class="_value _seconds">00</span>'
        '<span class="_delim _space">&nbsp;</span>'
        '<span class="_tzname">UTC</span>'
        '</div>')
