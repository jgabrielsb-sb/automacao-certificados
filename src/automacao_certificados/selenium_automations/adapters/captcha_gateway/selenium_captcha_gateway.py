
from automacao_certificados.selenium_automations.core.interfaces.captcha_gateway import SeleniumCaptchaGatewayPort
from automacao_certificados.selenium_automations.adapters.ui.selenium.utils import (
    get_image_as_base64,
)

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_package.actions import *
from selenium_package.executors import *
from selenium_package.interfaces import BaseExecutor

from typing import Tuple

class SeleniumCaptchaGateway(SeleniumCaptchaGatewayPort):
    def __init__(
        self,
        webdriver: WebDriver,
    ):
        if not isinstance(webdriver, WebDriver):
            raise ValueError("webdriver must be a Webdriver")

        self.webdriver = webdriver

    def get_captcha_base64_img(self, img_webelement) -> str:
        base64_img = get_image_as_base64(img_webelement)
        return base64_img

    def fill_captcha_text(self, input_webelement, text: str) -> None:
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

        

    


    

    

    

    