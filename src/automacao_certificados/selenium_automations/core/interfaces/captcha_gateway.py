from typing import Protocol, runtime_checkable

from pydantic import BaseModel

@runtime_checkable
class SeleniumCaptchaGatewayPort(Protocol):
    """
    Interface responsible for defining the contract for selenium captcha gateways.
    """
    def get_captcha_base64_img(self, img_webelement) -> str:
        """
        Gets the captcha base64 image.
        
        :param img_webelement: the image web element.
        :type img_webelement: WebElement
        :return: the captcha base64 image.
        :rtype: str
        """
    def fill_captcha_text(self, input_webelement, text: str) -> None:
        """
        Fills the captcha text.
        
        :param input_webelement: the input web element.
        :type input_webelement: WebElement
        :param text: the text to fill.
        :type text: str
        :return: None
        :rtype: None
        """