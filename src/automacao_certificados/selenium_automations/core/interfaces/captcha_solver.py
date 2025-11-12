from pydantic import BaseModel

from typing import Protocol

class CaptchaSolverInput(BaseModel):
    pass

class CaptchaSolverPort(Protocol):
    def solve_captcha(self, input: CaptchaSolverInput) -> None: ...
