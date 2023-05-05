import pytest
from selenium import webdriver
from typing import Literal
from src.data import DataWriterBase
from src.data.utils import WebDriverBuilder
from src.data.shikimori import ShikimoriAnimeParser


@pytest.fixture
def parser():
    builder = WebDriverBuilder('chrome', False)
    writer_mock = DataWriterBase()
    anime_parser = ShikimoriAnimeParser(
        builder(), 'https://shikimori.me', 1, writer_mock)
    return anime_parser


@pytest.mark.skip(reason="Might not work on all devices")
@pytest.mark.parametrize("browser_name, is_headless", [("chrome", False), ("chrome", True)])
def test_web_driver_launches(browser_name: Literal["chrome", "edge"], is_headless: bool):
    driver = WebDriverBuilder(browser_name, is_headless)()
    assert isinstance(driver, webdriver.Chrome if browser_name ==
                      "chrome" else webdriver.Edge)
    driver.quit()


def test_single_page(parser: ShikimoriAnimeParser):
    result = parser.get_anime_data(1)
    assert result is not None
