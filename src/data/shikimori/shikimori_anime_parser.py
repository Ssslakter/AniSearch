import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

from utils import WebParserParams
import data_writers as data_writers


class ShikimoriAnimeParser:
    def __init__(self, params: WebParserParams, url: str, max_pages: int, data_writer: data_writers.DataWriter) -> None:
        self.url = url
        self.browser = webdriver.Chrome(
            service=params.service, options=params.options)
        self.max_pages = max_pages
        self.data_writer = data_writer

    def get_ids(self, page_number: int) -> list[str]:
        self.browser.get(f"{self.url}/animes/page/{page_number}")
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        anime_list = soup.find_all("article", {"class": "c-anime"})

        return list(map(lambda x: x["id"], anime_list))

    def get_anime_data(self, anime_id: str) -> tuple[str | None, list[str]]:
        uri = f"{self.url}/animes/z{anime_id}"
        self.browser.get(uri)
        time.sleep(2)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        genres = soup.find_all("span", {"class": "genre-ru"})
        header = soup.find("header", {"class": "head"})
        label = header.find("h1").text if header else None
        ru_name, en_name = label.split(" / ") if label else (None, None)
        genres = list(map(lambda x: x.text, genres))

        return {"id": anime_id, "ru_name": ru_name, "en_name": en_name, "genres": genres}

    def parse(self) -> None:
        self.data_writer.prepare()
        for i in range(1, self.max_pages+1):
            print(f"Parsing {i} page")
            page_ids = self.get_ids(i)
            for anime_id in tqdm(page_ids):
                anime_data = self.get_anime_data(anime_id)
                self.data_writer.write(anime_data)
                break
        self.data_writer.finalize()
        print("Successfully parsed all data!")


if __name__ == "__main__":
    params = WebParserParams("--headless")
    writer = data_writers.JsonWriter("data/anime.json")
    anime_parser = ShikimoriAnimeParser(
        params, "https://shikimori.one", 1, writer)
    anime_parser.parse()
