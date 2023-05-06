import pytest
from unittest.mock import Mock
from selenium import webdriver
from typing import Literal
from src.data.utils import DataWriterBase, WebDriverBuilder
from src.data.shikimori import ShikimoriAnimeParser


@pytest.mark.dependency()
def test_chrome_driver_launches():
    driver = WebDriverBuilder('chrome', False)()
    assert isinstance(driver, webdriver.Chrome)
    driver.quit()


class TestParser:

    @pytest.fixture
    def chrome_parser(self):
        builder = WebDriverBuilder('chrome', False)
        writer_mock = Mock(spec=DataWriterBase)
        anime_parser = ShikimoriAnimeParser(
            builder(), 'https://shikimori.me', 1, writer_mock)
        return anime_parser

    @pytest.mark.dependency(depends=["test_chrome_driver_launches"])
    def test_single_page(self, chrome_parser: ShikimoriAnimeParser):
        result = chrome_parser.get_anime_data(1)
        assert result is not None
