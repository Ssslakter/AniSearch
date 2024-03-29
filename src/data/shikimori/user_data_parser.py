import json
import time
import uuid
from venv import logger
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests


MAX_PAGES = 100


class ShikimoriUserDataParser:
    """Parses user ratings data from shikimori"""

    def __init__(self, url: str, max_users: int) -> None:
        self.headers = {"User-Agent": ""}
        self.url = url
        self.max_users = max_users
        self.max_pages = MAX_PAGES

    def get_users(self, page_number: int) -> list[str]:
        """Get userpage urls from a page

        Args:
            page_number (int): number of the page to parse

        Returns:
            list[str]: list of userpage urls
        """
        response = requests.get(
            f"{self.url}/users/page/{page_number}", headers=self.headers, timeout=10
        )
        soup = BeautifulSoup(response.text, "html.parser")

        user_links = []
        user_divs = soup.find_all("div", {"class": "b-user"})

        user_links = list(map(lambda x: x.find("a", class_="name")["href"], user_divs))

        return user_links

    def get_user_anime_list(self, user_url: str) -> list[dict]:
        """Gets anime list of a user

        Args:
            user_url (str): url of the page user

        Returns:
            list[dict]: list of user-anime data
        """
        url = f"{user_url}/list_export/animes.json"
        response = requests.get(url, headers=self.headers, timeout=10)

        return json.loads(response.text)

    def parse(self) -> tuple[dict, list[int]]:
        """Start parsing user data

        Returns:
            tuple[dict, list[int]]: dictionary of data and list of failed urls
        """
        failed = []
        data = {}
        pbar = tqdm(total=self.max_users)
        for i in range(MAX_PAGES):
            user_urls = self.get_users(i)

            for url in user_urls:
                try:
                    user_data = self.get_user_anime_list(url)
                    if user_data:
                        data[str(uuid.uuid4())] = user_data
                        pbar.update(1)
                    if len(data) == self.max_users:
                        pbar.close()
                        return data, failed
                    # sleep to not get captcha
                    time.sleep(2.5)
                except AttributeError:
                    logger.error("\nFailed to parse page with url %s", url)
                    failed.append(url)
        pbar.close()
        return data, failed
