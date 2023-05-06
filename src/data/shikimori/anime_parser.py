import time
from venv import logger
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from src.data.utils import DataWriterBase


class ShikimoriAnimeParser:
    """Class for parsing shikimori anime data

    """

    def __init__(self, webdriver: WebDriver, url: str, max_pages: int, data_writer: DataWriterBase) -> None:
        """ShikimoriAnimeParser constructor

        Args:
            webdriver (webdriver): selenium webdriver to execute
            url (str): url of the shikimori website
            max_pages (int): maximum number of pages to parse
            data_writer (data_writers.DataWriterBase): data-writer to save the parsed data
        """
        self.url = url
        self.webdriver = webdriver
        self.max_pages = max_pages
        self.data_writer = data_writer

    def get_ids(self, page_number: int) -> list[str]:
        """gets ids of anime on a page

        Args:
            page_number (int): number of the web page

        Returns:
            list[str]: list of anime ids
        """
        self.webdriver.get(f"{self.url}/animes/page/{page_number}")
        soup = BeautifulSoup(self.webdriver.page_source, 'html.parser')
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
        self.webdriver.get(uri)
        soup = BeautifulSoup(self.webdriver.page_source, 'html.parser')

        return {"id": anime_id} | self._parse_page(soup)

    def _parse_page(self, page: BeautifulSoup) -> dict[str, object]:

        genres = page.find_all("span", {"class": "genre-ru"})
        header = page.find("header", {"class": "head"})
        label = header.find("h1").text if header else None
        ru_name, en_name = label.split(" / ") if label else (None, None)
        genres = list(map(lambda x: x.text, genres))

        episodes_div = page.find('div', class_='key', text='Эпизоды:').parent
        number = episodes_div.find('div', class_='value').text

        type_div = page.find('div', class_='key', text='Тип:').parent
        type_value = type_div.find('div', class_='value').text

        scores_div = page.find('div', class_='scores')
        score_value_div = scores_div.find('div', class_='score-value')
        score_value = float(score_value_div.text.strip())

        age_div = page.find('div', class_='key', text='Рейтинг:').parent
        age_value = age_div.find('div', class_='value').text

        return {
            "ru_name": ru_name,
            "en_name": en_name,
            "genres": genres,
            "episode_number": number,
            "content_type": type_value,
            "average_score": score_value,
            "age": age_value
        }

    def parse(self) -> list[int]:
        """Function that starts parcing the website

        Returns:
            list[int]: list of ids failed to parse
        """
        failed = []
        self.data_writer.prepare()
        for i in range(1, self.max_pages+1):

            logger.info(f"Parsing {i} page")
            page_ids = self.get_ids(i)

            for anime_id in tqdm(page_ids):
                try:
                    anime_data = self.get_anime_data(anime_id)
                    self.data_writer.write(anime_data)
                    # sleep to not get captcha
                    time.sleep(2.5)
                except Exception as e:
                    logger.error(f"Failed to parse page with id {anime_id}")
                    failed.append(anime_id)
        self.data_writer.finalize()
        return failed
