from selenium.webdriver.remote.webdriver import WebDriver

from abc import ABC, abstractmethod

class BasePage(ABC):
    """
    Base class for all page objects.
    """
    def __init__(self, driver: WebDriver):
        if not isinstance(driver, WebDriver):
            raise ValueError("driver must be a WebDriver")

        self.driver = driver