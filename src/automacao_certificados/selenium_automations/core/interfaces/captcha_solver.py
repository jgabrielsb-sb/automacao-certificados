from pydantic import BaseModel, ConfigDict

from typing import Protocol, Optional

from selenium.webdriver.remote.webelement import WebElement

class CaptchaSolverInput(BaseModel):
    img_webelement: Optional[WebElement]
    input_webelement: Optional[WebElement]

    model_config = ConfigDict(arbitrary_types_allowed=True)

class CaptchaSolverPort(Protocol):
    def solve_captcha(self, input: CaptchaSolverInput) -> None: ...
