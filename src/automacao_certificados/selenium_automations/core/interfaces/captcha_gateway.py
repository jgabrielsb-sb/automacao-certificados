from typing import Protocol, runtime_checkable

from pydantic import BaseModel

class FillCaptchaTextResult(BaseModel):
    retries: int
    how_many_seconds_took: int

@runtime_checkable
class CaptchaGatewayPort(Protocol):
    def get_captcha_base64_img(self) -> str: ...
    def fill_captcha_text(self, text: str) -> FillCaptchaTextResult: ...