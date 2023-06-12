import time
from venv import logger
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests


class ShikimoriAnimeParser:
    """Class for parsing shikimori anime data"""

    def __init__(self, url: str, max_pages: int) -> None:
        """ShikimoriAnimeParser constructor

        Args:
            webdriver (webdriver): selenium webdriver to execute
            url (str): url of the shikimori website
            max_pages (int): maximum number of pages to parse
        """
        self.url = url
        self.headers = {"User-Agent": ""}
        self.max_pages = max_pages

    def get_ids(self, page_number: int) -> list[str]:
        """gets ids of anime on a page

        Args:
            page_number (int): number of the web page

        Returns:
            list[str]: list of anime ids
        """
        response = requests.get(
            f"{self.url}/animes/page/{page_number}", headers=self.headers, timeout=10
        )
        soup = BeautifulSoup(response.text, "html.parser")
        anime_list = soup.find_all("article", {"class": "c-anime"})

        return list(map(lambda x: x["id"], anime_list))

    def get_anime_data(self, anime_id: str) -> dict[str, object]:
        """Gets anime data from its main page

        Args:
            anime_id (str): id of the anime on the shikimori to join its page

        Returns:
            dict[str, object]: dictionary of properties extracted from page
        """
        uri = f"{self.url}/animes/z{anime_id}"
        response = requests.get(uri, headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        return self._parse_page(soup)

    def _parse_page(self, page: BeautifulSoup) -> dict[str, object]:
        genres = page.find_all("span", {"class": "genre-ru"})
        header = page.find("header", {"class": "head"})
        label = header.find("h1").text if header else None
        ru_name, en_name = label.split(" / ") if label else (None, None)
        genres = list(map(lambda x: x.text, genres))

        episodes_div = page.find("div", class_="key", text="Эпизоды:").parent
        number = episodes_div.find("div", class_="value").text

        type_div = page.find("div", class_="key", text="Тип:").parent
        type_value = type_div.find("div", class_="value").text

        scores_div = page.find("div", class_="scores")
        score_value_div = scores_div.find("div", class_="score-value")
        score_value = float(score_value_div.text.strip())

        age_div = page.find("div", class_="key", text="Рейтинг:").parent
        age_value = age_div.find("div", class_="value").text

        return {
            "ru_name": ru_name,
            "en_name": en_name,
            "genres": genres,
            "episode_number": number,
            "content_type": type_value,
            "average_score": score_value,
            "age": age_value,
        }

    def parse(self) -> tuple[dict, list[int]]:
        """Function that starts parcing the website

        Returns:
            Tuple[dict, list[int]]: dictionary with data and list of ids failed to parse
        """
        failed = []
        data = {}
        for i in range(1, self.max_pages + 1):
            logger.info("Parsing %s page", i)
            page_ids = self.get_ids(i)

            for anime_id in tqdm(page_ids):
                try:
                    anime_data = self.get_anime_data(anime_id)
                    data[anime_id] = anime_data
                    # sleep to not get captcha
                    time.sleep(2.5)
                except AttributeError:
                    logger.error("Failed to parse page with id %s", anime_id)
                    failed.append(anime_id)
        return data, failed
