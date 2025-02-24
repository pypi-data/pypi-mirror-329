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



def test_datagrid(
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
        {content.scripts('datagrid')}
            </script>
          </head>
          <body></body>
        </html>
        """)


    fields = {
        'foo': 'Foo',
        'bar': 'Bar'}

    values = [
        {'foo': '1',
         'bar': 1},
        {'foo': '2',
         'bar': 2}]


    outcome = _executejs(
        driver,
        'let element ='
        ' datagrid(...arguments);'
        'return'
        ' element[0].outerHTML;',
        fields,
        values,
        wrap=False)


    assert outcome == (
        '<table class="encommon_datagrid">'
        '<thead>'
        '<tr>'
        '<th>Bar</th>'
        '<th>Foo</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
        '<tr>'
        '<td>1</td>'
        '<td>1</td>'
        '</tr>'
        '<tr>'
        '<td>2</td>'
        '<td>2</td>'
        '</tr>'
        '</tbody>'
        '</table>')
