import time
import uuid
from venv import logger
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from tqdm import tqdm

from src.data.utils import DataWriterBase


class ShikimoriUserDataParser:
    """Parses user ratings data from shikimori
    """

    def __init__(self, webdriver: WebDriver, url: str, max_pages: int, data_writer: DataWriterBase) -> None:
        self.webdriver = webdriver
        self.url = url
        self.max_pages = max_pages
        self.data_writer = data_writer

    def get_users(self, page_number: int) -> list[str]:
        """Get userpage urls from a page

        Args:
            page_number (int): number of the page to parse

        Returns:
            list[str]: list of userpage urls
        """
        self.webdriver.get(f"{self.url}/users/page/{page_number}")
        soup = BeautifulSoup(self.webdriver.page_source, 'html.parser')

        user_links = []
        user_divs = soup.find_all("div", {"class": "b-user"})

        user_links = list(map(lambda x: x.find(
            'a', class_="name")["href"], user_divs))

        return user_links

    def get_user_anime_list(self, user_url: str) -> list[tuple[str, int | None]]:
        """Gets anime list of a user

        Args:
            user_url (str): url of the page user

        Returns:
            tuple[list[AnimeRating], list[str]]: tuple of anime list
        """
        url = f"{user_url}/list/anime"
        self.webdriver.get(url)
        soup = BeautifulSoup(self.webdriver.page_source, 'html.parser')
        watched = soup.find("div", text='Просмотрено')
        if watched is None:
            return []
        watched_table = watched.parent.find_next_sibling('table')

        user_rates = watched_table.find_all("tr", {"class": "user_rate"})
        rates_data = list(map(self._parse_row, user_rates))
        return rates_data

    def _parse_row(self, row: BeautifulSoup) -> tuple[str, int | None]:
        """Parses a row of the table

        Args:
            row (BeautifulSoup): row to parse

        Returns:
            dict[str, object]: parsed data
        """
        rating = row.find_next("span", {"class": "current-value"}).text
        rating = int(rating) if rating != "–" else None

        anime_id = f"{row['data-target_id']}"

        return (anime_id, rating)

    def parse(self) -> list[str]:
        """Start parsing user data

        Returns:
            list[int]: list of failed urls
        """
        failed = []
        self.data_writer.prepare()
        for i in range(1, self.max_pages+1):

            logger.info("Parsing %s page", i)
            user_urls = self.get_users(i)

            for url in tqdm(user_urls):
                try:
                    user_data = {
                        "user_id": str(uuid.uuid4()),
                        "ratings": self.get_user_anime_list(url)
                    }
                    self.data_writer.write(user_data)
                    # sleep to not get captcha
                    time.sleep(2.5)
                except AttributeError:
                    logger.error("Failed to parse page with url %s", url)
                    failed.append(url)
        self.data_writer.finalize()
        return failed
