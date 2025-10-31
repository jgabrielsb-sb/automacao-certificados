"""
Page object model for any page that contains a captcha.
A captcha page is a page that contains an image and an input field.
- The image is used to display a captcha to the user.
- The input field is used to enter the captcha text.
This page does not include the logic to get the captcha text from the image.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_package.actions import *
from selenium_package.executors import *
from selenium_package.interfaces import BaseExecutor

from automacao_certificados.selenium_automations.core.interfaces import (
    BaseImageProcessor,
    BasePage
)

from automacao_certificados.selenium_automations.adapters.ui.selenium.utils import (
    get_image_as_base64,
)

class CaptchaPage(BasePage):
    """
    Page object model for any page that contains a captcha.
    A captcha page is a page that contains an image and an input field.
    - The image is used to display a captcha to the user.
    - The input field is used to enter the captcha text.
    """

    def __init__(
        self,
        driver: WebDriver,
        img_web_element: WebElement,
        input_web_element: WebElement,
        image_processor: BaseImageProcessor,
    ):
        """
        Args:
            driver: The driver to use to interact with the page.
            img_web_element: The web element that contains the image.
            input_web_element: The web element that contains the input field.
        """
        if not isinstance(img_web_element, WebElement):
            raise ValueError("img_web_element must be a WebElement")

        if not isinstance(input_web_element, WebElement):
            raise ValueError("input_web_element must be a WebElement")

        if not isinstance(image_processor, BaseImageProcessor):
            raise ValueError("image_processor must be a BaseImageProcessor")

        super().__init__(driver)

        self.img_web_element = img_web_element
        self.input_web_element = input_web_element
        self.image_processor = image_processor

    def get_captcha_text(self) -> str:
        """
        Gets the captcha text from the image.
        Returns:
            str: The captcha text from the image.
        """
        image_base64 = get_image_as_base64(self.img_web_element)
        captcha_text = self.image_processor.get_text_from_image(image_base64)
        return captcha_text

    def insert_text_on_input_executor(self, text: str) -> BaseExecutor:
        """
        Inserts text on the input field.
        Args:
            text: The text to insert on the input field.
        Returns:
            BaseExecutor: The executor to insert text on the input field.
        Raises:
            ValueError: If text is not a string.
        """
        if not isinstance(text, str):
            raise ValueError("text must be a string")

        action = InsertText(
            web_instance=self.driver,
            web_element=self.input_web_element,
            text=text,
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=self.input_web_element,
            property_name="value",
            property_value=text,
        )

        return executor

    def solve_captcha(self) -> str:
        """
        Solves the captcha by getting the captcha text from the image 
        and inserting it on the input field.
        Returns:
            str: The captcha text.
        """
        captcha_text = self.get_captcha_text()
        self.insert_text_on_input_executor(captcha_text).run()
        return captcha_text