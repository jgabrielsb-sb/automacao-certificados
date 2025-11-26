
from automacao_certificados.selenium_automations.core.interfaces.captcha_gateway import SeleniumCaptchaGatewayPort
from automacao_certificados.selenium_automations.adapters.ui.selenium.utils import (
    get_image_as_base64,
)

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_package.actions import *
from selenium_package.executors import *
from selenium_package.interfaces import BaseExecutor

from typing import Tuple

class SeleniumCaptchaGateway(SeleniumCaptchaGatewayPort):
    def __init__(
        self,
        webdriver: WebDriver,
    ):
        """
        The selenium captcha gateway is an implementation of the selenium captcha gateway port 
        that uses selenium to get the captcha base64 image and fill the captcha text.
        """
        if not isinstance(webdriver, WebDriver):
            raise ValueError("webdriver must be a Webdriver")

        self.webdriver = webdriver

    def get_captcha_base64_img(self, img_webelement: WebElement) -> str:
        """
        Get the captcha base64 image from the image web element.

        :param img_webelement: The selenium image web element.
        :type img_webelement: WebElement
        :return: The captcha base64 image.
        :rtype: str
        """
        if not isinstance(img_webelement, WebElement):
            raise ValueError("img_webelement must be a WebElement")

        base64_img = get_image_as_base64(img_webelement)
        return base64_img

    def fill_captcha_text(self, input_webelement: WebElement, text: str) -> None:
        """
        Fill the captcha text in the input web element.

        :param input_webelement: The selenium input web element.
        :type input_webelement: WebElement
        :param text: The text to fill.
        :type text: str
        :return: None
        :rtype: None
        """
        if not isinstance(input_webelement, WebElement):
            raise ValueError("input_webelement must be a WebElement")

        if not isinstance(text, str):
            raise ValueError("text must be a string")

        action = InsertText(
            web_instance=self.webdriver,
            web_element=input_webelement,
            text=text,
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=input_webelement,
            property_name="value",
            property_value=text,
        ).run()

        

    


    

    

    

    