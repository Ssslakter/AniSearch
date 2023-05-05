import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Literal
from src.data.utils import WebDriverBuilder


@pytest.mark.skip(reason="Might not work on all devices")
@pytest.mark.parametrize("browser_name, is_headless", [("chrome", False), ("chrome", True)])
def test_web_driver_launches(browser_name: Literal["chrome", "edge"], is_headless: bool):
    driver = WebDriverBuilder(browser_name, is_headless)()
    assert isinstance(driver, webdriver.Chrome if browser_name ==
                      "chrome" else webdriver.Edge)
    driver.quit()
