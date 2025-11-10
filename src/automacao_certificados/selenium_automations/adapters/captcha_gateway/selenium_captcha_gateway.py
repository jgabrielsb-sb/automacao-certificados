
from automacao_certificados.selenium_automations.core.interfaces.captcha_gateway import CaptchaGatewayPort
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

class SeleniumCaptchaGateway(CaptchaGatewayPort):
    def __init__(
        self,
        webdriver: WebDriver,
        img_locator: Tuple[By, str],
        input_locator: Tuple[By, str],
        wait_for: int = 5
    ):
        if not isinstance(webdriver, WebDriver):
            raise ValueError("webdriver must be a Webdriver")

        if not isinstance(wait_for, int):
            raise ValueError("wait_for must be an integer")

        self.webdriver = webdriver
        self.wait_for = wait_for
        self.input_locator = input_locator
        self.img_locator = img_locator

    def _get_input_web_element(self):
        return WebDriverWait(self.driver, self.wait_for).until(
            EC.presence_of_element_located(self.input_locator)
        )

    def _get_img_web_element(self):
        return WebDriverWait(self.driver, self.wait_for).until(
            EC.presence_of_element_located(self.img_locator)
        )

    def get_captcha_base64_img(self) -> str:
        img_web_element = self._get_img_web_element()
        base64_img = get_image_as_base64(img_web_element)
        return base64_img

    def fill_captcha_text(self, text: str) -> None:
        if not isinstance(text, str):
            raise ValueError("text must be a string")

        input_web_element = self._get_input_web_element()

        action = InsertText(
            web_instance=self.webdriver,
            web_element=input_web_element,
            text=text,
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=input_web_element,
            property_name="value",
            property_value=text,
        )

        return executor

    


    

    

    

    