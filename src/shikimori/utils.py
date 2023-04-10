from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class AnimeRating:
    def __init__(self, animeId: str, userLink: str, rating: int | None) -> None:
        self.animeId = animeId
        self.userLink = userLink
        self.rating = rating


class WebParserParams:
    def __init__(self, *option_args) -> None:
        self.service = Service(executable_path="chromedriver")
        self.options = Options()
        for arg in option_args:
            self.options.add_argument(arg)
