import time
from bs4 import BeautifulSoup
from selenium import webdriver

from utils import AnimeRating, WebParserParams


class ShikimoriUserDataParser:
    def __init__(self, params: WebParserParams) -> None:
        self.browser = webdriver.Chrome(
            service=params.service, options=params.options)

    def get_users(self, anime_url: str) -> list[str]:
        url = f"{anime_url}/favoured"
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        user_links = []
        users_el = soup.find_all("a", {"class": "avatar"})

        for user in users_el:
            user_links.append(user["href"])

        return user_links

    def get_user_anime_list(self, user_url: str) -> tuple[list[AnimeRating], list[str]]:
        url = f"{user_url}/list/anime"
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        anime_list_el = soup.find_all("tr", {"class": "user_rate"})

        rates, anime = [], []

        for el in anime_list_el:
            rating = el.find_next("span", {"class": "current-value"}).text
            rating = int(rating) if rating != "–" else None

            anime_id = f"z{el['data-target_id']}"

            rates.append(AnimeRating(anime_id, user_url, rating))
            anime.append(anime_id)

        return rates, anime

    def wait_for_login(self) -> None:
        self.browser.get("https://shikimori.one")
        time.sleep(20)


# def update_anime_collection(anime_list: list[str]) -> None:
#     global anime

#     for an in anime_list:
#         if an in anime:
#             continue

#         anime.append(an)


# ratings = []
# anime = []
# tags = ['Психологическое', 'Этти', 'Романтика', 'Повседневность', 'Сверхъестественное', 'Пародия', 'Школа',
#         'Демоны', 'Спорт', 'Игры', 'Меха', 'Исторический', 'Супер сила', 'Сэйнэн', 'Безумие', 'Самураи',
#         'Сёнен', 'Дзёсей', 'Боевые искусства', 'Приключения', 'Вампиры', 'Сёдзё', 'Ужасы', 'Музыка',
#         'Гурман', 'Драма', 'Фантастика', 'Триллер', 'Фэнтези', 'Военное', 'Детектив', 'Полиция',
#         'Экшен', 'Работа', 'Комедия', 'Космос', 'Сёдзё-ай', 'Гарем'
#         ]


# def complex_parse() -> None:
#     global ratings, anime, tags

#     wait_for_login()
#     users = get_users("https://shikimori.one/animes/2559-romeo-no-aoi-sora")

#     for user in users:
#         time.sleep(2)

#         r, a = get_user_anime_list(user)
#         ratings += r
#         update_anime_collection(a)

#     init_anime_csv()
#     save_anime()


# ANIME_PAGE = 1
