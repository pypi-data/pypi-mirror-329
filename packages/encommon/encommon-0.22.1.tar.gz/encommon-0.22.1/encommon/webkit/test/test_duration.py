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



def test_duration(
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
        {content.scripts('duration')}
            </script>
          </head>
          <body></body>
        </html>
        """)


    outcome = _executejs(
        driver,
        'let element ='
        ' duration(...arguments);'
        'return'
        ' element[0].outerHTML;',
        90460023,
        wrap=False)


    assert outcome == (
        '<div class="encommon_duration">'
        '<span class="_value">2</span>'
        '<span class="_unit">y</span>'
        '<span class="_value">10</span>'
        '<span class="_unit">mon</span>'
        '<span class="_value">2</span>'
        '<span class="_unit">w</span>'
        '<span class="_value">2</span>'
        '<span class="_unit">d</span>'
        '<span class="_value">23</span>'
        '<span class="_unit">h</span>'
        '<span class="_value">47</span>'
        '<span class="_unit">m</span>'
        '</div>')
