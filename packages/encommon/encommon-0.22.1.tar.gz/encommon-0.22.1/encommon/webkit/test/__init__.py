"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver



def _executejs(
    driver: WebDriver,
    script: str,
    *args: Any,
    wrap: bool = True,
) -> Any:  # noqa: ANN401
    """
    Evaluate the provided JavaScript using the test driver.

    :param driver: Selenium driver provided by the library.
    :param script: Actual code that is executed with engine.
    :param args: Positional arguments passed for downstream.
    :param wrap: Determines if script is wrapped in return.
    """

    script = (
        f'return {script};'
        if wrap else script)

    result = (
        driver  # type: ignore[no-untyped-call]
        .execute_script(script, *args))

    return result
