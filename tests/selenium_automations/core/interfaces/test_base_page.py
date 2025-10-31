import pytest
from unittest.mock import Mock

from automacao_certificados.selenium_automations.core.interfaces import BasePage

@pytest.fixture
def base_page_class() -> type[BasePage]:
    """
    Fixture to create a BasePage instance.
    """
    class MockBasePage(BasePage):
        """
        Mock class for the BasePage interface.
        """
        pass

    return MockBasePage

class TestBasePage:
    """
    Test class for the BasePage interface.
    """
    def test_if_raises_value_error_if_driver_is_not_a_webdriver(
        self,
        base_page_class: type[BasePage],
    ):
        """
        Test if the BasePage raises a ValueError if the driver is not a WebDriver.
        """
        with pytest.raises(ValueError):
            base_page_class(driver=123)

    def test_if_initializes_the_driver_with_chrome_webdriver(
        self,
        base_page_class: type[BasePage],
    ):
        """
        Test if the BasePage initializes the driver.
        """
        from selenium.webdriver.chrome.webdriver import WebDriver
        base_page_class(
            driver=Mock(WebDriver)
        )

    def test_if_initializes_the_driver_with_firefox_webdriver(
        self,
        base_page_class: type[BasePage],
    ):
        """
        Test if the BasePage initializes the driver.
        """
        from selenium.webdriver.firefox.webdriver import WebDriver
        base_page_class(
            driver=Mock(WebDriver)
        )

    
        