"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Iterator

from pytest import fixture

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from ..content import Content



@fixture
def content() -> Content:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return Content()



@fixture
def driver() -> Iterator[WebDriver]:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    options = Options()

    options.add_argument('--headless')

    driver = (
        webdriver
        .Chrome(options=options))

    yield driver

    driver.quit()
