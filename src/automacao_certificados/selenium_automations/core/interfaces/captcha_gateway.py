from typing import Protocol, runtime_checkable

from pydantic import BaseModel

@runtime_checkable
class CaptchaGatewayPort(Protocol):
    def get_captcha_base64_img(self, img_webelement) -> str: ...
    def fill_captcha_text(self, input_webelement, text: str) -> None: ...