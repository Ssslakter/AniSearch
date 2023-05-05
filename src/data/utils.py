from typing import Literal
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import EdgeOptions, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


class WebDriverBuilder:
    """Class to simplify creation of Selenium webdrivers
    """

    def __init__(self, browser_name: Literal["chrome", "edge"] = "chrome", open_window: bool = True) -> None:
        match browser_name:
            case "chrome":
                options = ChromeOptions()
                service = ChromeService(executable_path="chromedriver")
                if not open_window:
                    options.add_argument("--headless")
                self.driver = webdriver.Chrome(
                    options=options, service=service)
            case "edge":
                options = EdgeOptions()
                service = EdgeService(executable_path="edgeedriver")
                if not open_window:
                    options.add_argument("--headless")
                self.driver = webdriver.Edge(options=options, service=service)

    def __call__(self) -> WebDriver:
        return self.driver
