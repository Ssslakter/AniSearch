import pytest
from unittest.mock import Mock
from selenium import webdriver
from src.data.shikimori import ShikimoriUserDataParser
from src.data.utils import DataWriterBase, WebDriverBuilder
from src.data.shikimori import ShikimoriAnimeParser

URL = 'https://shikimori.me'


@pytest.mark.dependency()
def test_chrome_driver_launches():
    driver = WebDriverBuilder('chrome', False)()
    assert isinstance(driver, webdriver.Chrome)
    driver.quit()


class TestParser:

    @pytest.fixture
    def anime_parser_chrome(self):
        builder = WebDriverBuilder('chrome', False)
        writer_mock = Mock(spec=DataWriterBase)
        anime_parser = ShikimoriAnimeParser(
            builder(), URL, 1, writer_mock)
        return anime_parser

    @pytest.fixture
    def user_parser_chrome(self):
        builder = WebDriverBuilder('chrome', False)
        writer_mock = Mock(spec=DataWriterBase)
        anime_parser = ShikimoriUserDataParser(
            builder(), URL, 1, writer_mock)
        return anime_parser

    @pytest.mark.dependency(depends=["test_chrome_driver_launches"])
    def test_sample_page_anime(self, anime_parser_chrome: ShikimoriAnimeParser):
        result = anime_parser_chrome.get_anime_data(1)
        assert result is not None

    @pytest.mark.dependency(depends=["test_chrome_driver_launches"])
    def test_users_page(self, user_parser_chrome: ShikimoriUserDataParser):
        result = user_parser_chrome.get_users(1)
        assert result is not None

    @pytest.mark.dependency(depends=["test_chrome_driver_launches"])
    def test_sample_user_page(self, user_parser_chrome: ShikimoriUserDataParser):
        result = user_parser_chrome.get_user_anime_list(
            f'{URL}/slakter')
        assert type(result) is list
        assert type(result[0]) is tuple

    @pytest.mark.dependency(depends=["test_chrome_driver_launches"])
    def test_empty_user_page_not_crash(self, user_parser_chrome: ShikimoriUserDataParser):
        result = user_parser_chrome.get_user_anime_list(
            f'{URL}/4rchm4g3')
        assert result == []
