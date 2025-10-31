import pytest

from unittest.mock import MagicMock

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from automacao_certificados.selenium_automations.adapters.ui.selenium.pages import (
    CaptchaPage,
)

from automacao_certificados.selenium_automations.core.interfaces import (
    BaseImageProcessor,
    BasePage,
)

class TestCaptchaPage:
    """
    Test class for the CaptchaPage class.
    """
    def test_if_raises_value_error_if_driver_is_not_a_web_driver(self):
        """
        Test if the CaptchaPage raises a ValueError if the driver is not a WebDriver.
        """
        
        with pytest.raises(ValueError):
            CaptchaPage(
                driver="not_a_web_driver",
                img_web_element=MagicMock(spec=WebElement),
                input_web_element=MagicMock(spec=WebElement),
                image_processor=MagicMock(spec=BaseImageProcessor),
            )

    def test_if_raises_value_error_if_img_web_element_is_not_a_web_element(self):
        """
        Test if the CaptchaPage raises a ValueError if the img_web_element is not a WebElement.
        """
        with pytest.raises(ValueError) as e:
            CaptchaPage(
                driver=MagicMock(spec=WebDriver),
                img_web_element="not_a_web_element",
                input_web_element=MagicMock(spec=WebElement),
                image_processor=MagicMock(spec=BaseImageProcessor),
            )

        assert "img_web_element" in str(e.value) 

    def test_if_raises_value_error_if_input_web_element_is_not_a_web_element(self):
        """
        Test if the CaptchaPage raises a ValueError if the input_web_element is not a WebElement.
        """
        with pytest.raises(ValueError) as e:
            CaptchaPage(
                driver=MagicMock(spec=WebDriver),
                img_web_element=MagicMock(spec=WebElement),
                input_web_element="not_a_web_element",
                image_processor=MagicMock(spec=BaseImageProcessor),
            )

        assert "input_web_element" in str(e.value) 

    def test_if_raises_value_error_if_image_processor_is_not_a_base_image_processor(self):
        """
        Test if the CaptchaPage raises a ValueError if the image_processor is not a BaseImageProcessor.
        """
        with pytest.raises(ValueError) as e:
            CaptchaPage(
                driver=MagicMock(spec=WebDriver),
                img_web_element=MagicMock(spec=WebElement),
                input_web_element=MagicMock(spec=WebElement),
                image_processor="not_a_base_image_processor",
            )

        assert "image_processor" in str(e.value) 