import pytest
from src.data.shikimori import ShikimoriUserDataParser, ShikimoriAnimeParser, SHIKIMORI_URL


class TestParser:

    @pytest.fixture
    def anime_parser(self):
        anime_parser = ShikimoriAnimeParser(SHIKIMORI_URL, 1)
        return anime_parser

    @pytest.fixture
    def user_parser(self):
        user_parser = ShikimoriUserDataParser(SHIKIMORI_URL, 1)
        return user_parser

    def test_sample_page_anime(self, anime_parser: ShikimoriAnimeParser):
        result = anime_parser.get_anime_data(1)
        assert result is not None

    def test_users_page(self, user_parser: ShikimoriUserDataParser):
        result = user_parser.get_users(1)
        assert result is not None

    def test_sample_user_page(self, user_parser: ShikimoriUserDataParser):
        result = user_parser.get_user_anime_list(
            f'{SHIKIMORI_URL}/slakter')
        assert type(result) is list
        assert type(result[0]) is dict

    def test_empty_user_page_not_crash(self, user_parser: ShikimoriUserDataParser):
        result = user_parser.get_user_anime_list(
            f'{SHIKIMORI_URL}/4rchm4g3')
        assert result == []
