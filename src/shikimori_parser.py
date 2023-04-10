import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class AnimeRating:
    def __init__(self, animeId: str, userLink: str, rating: int | None) -> None:
        self.animeId = animeId
        self.userLink = userLink
        self.rating = rating


service = Service(executable_path="chromedriver")
options = Options()
# options.add_argument("--headless")
browser = webdriver.Chrome(service=service, options=options)


def get_users(anime_url: str) -> list[str]:
    url = f"{anime_url}/favoured"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    user_links = []
    users_el = soup.find_all("a", {"class": "avatar"})

    for user in users_el:
        user_links.append(user["href"])

    return user_links


def get_user_anime_list(user_url: str) -> tuple[list[AnimeRating], list[str]]:
    url = f"{user_url}/list/anime"
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    anime_list_el = soup.find_all("tr", {"class": "user_rate"})

    rates, anime = [], []

    for el in anime_list_el:
        rating = el.find_next("span", {"class": "current-value"}).text
        rating = int(rating) if rating != "–" else None

        anime_id = f"z{el['data-target_id']}"

        rates.append(AnimeRating(anime_id, user_url, rating))
        anime.append(anime_id)

    return rates, anime


def get_anime_data(anime_url: str) -> tuple[str | None, list[str]]:
    global tags

    browser.get(anime_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    genres = soup.find_all("span", {"class": "genre-ru"})
    header = soup.find("header", {"class": "head"})
    label = header.find("h1").text if header is not None else None

    for i, genre in enumerate(genres):
        genres[i] = genre.text

    return label, genres


def update_anime_collection(anime_list: list[str]) -> None:
    global anime

    for an in anime_list:
        if an in anime:
            continue

        anime.append(an)


def save_anime_csv(anime_id: str, anime_name: str, anime_genres: list[str]) -> None:
    global tags

    with open("anime.csv", "a", encoding="utf-8") as f:
        data = f"{anime_id},{anime_name},"
        for tag in tags:
            data += f"{tag in anime_genres},"

        data = data[:-1] + "\n"

        f.write(data)


def init_anime_csv() -> None:
    global tags

    with open("anime.csv", "w", encoding="utf-8") as f:
        f.write(f"Идентификатор,Название,{','.join(tags)}\n")


def wait_for_login() -> None:
    browser.get("https://shikimori.one")
    time.sleep(20)


def get_anime_list(url: str) -> list[str]:
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    anime_list = soup.find_all("article", {"class": "c-anime"})
    for i, an in enumerate(anime_list):
        anime_list[i] = f"z{an['id']}"

    return anime_list


ratings = []
anime = []
tags = ['Психологическое', 'Этти', 'Романтика', 'Повседневность', 'Сверхъестественное', 'Пародия', 'Школа',
        'Демоны', 'Спорт', 'Игры', 'Меха', 'Исторический', 'Супер сила', 'Сэйнэн', 'Безумие', 'Самураи',
        'Сёнен', 'Дзёсей', 'Боевые искусства', 'Приключения', 'Вампиры', 'Сёдзё', 'Ужасы', 'Музыка',
        'Гурман', 'Драма', 'Фантастика', 'Триллер', 'Фэнтези', 'Военное', 'Детектив', 'Полиция',
        'Экшен', 'Работа', 'Комедия', 'Космос', 'Сёдзё-ай', 'Гарем'
        ]


def complex_parse() -> None:
    global ratings, anime, tags

    wait_for_login()
    users = get_users("https://shikimori.one/animes/2559-romeo-no-aoi-sora")

    for user in users:
        time.sleep(2)

        r, a = get_user_anime_list(user)
        ratings += r
        update_anime_collection(a)

    init_anime_csv()
    save_anime()


def save_anime() -> None:
    global anime

    for anime_id in anime:
        time.sleep(2)

        data = get_anime_data(f"https://shikimori.one/animes/{anime_id}")
        save_anime_csv(anime_id, data[0], data[1])


ANIME_PAGE = 1

if __name__ == "__main__":
    for i in range(ANIME_PAGE, 10):
        print(f"Parsing anime page № {i}")
        anime += get_anime_list(f"https://shikimori.one/animes/page/{i}")

    init_anime_csv()
    save_anime()


