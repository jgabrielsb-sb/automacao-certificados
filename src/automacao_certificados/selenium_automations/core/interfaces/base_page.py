from selenium.webdriver.remote.webdriver import WebDriver

from abc import ABC, abstractmethod

class BasePage(ABC):
    """
    Interface responsible for defining the contract for base pages.
    """
    def __init__(self, driver: WebDriver):
        if not isinstance(driver, WebDriver):
            raise ValueError("driver must be a WebDriver")

        self.driver = driver