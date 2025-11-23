

import pytest

from selenium.webdriver.remote.webelement import WebElement
from unittest.mock import MagicMock

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

@pytest.fixture
def captcha_solver_port():
    class CaptchaSolverPortImpl(CaptchaSolverPort):
        def _solve_captcha(self, input: CaptchaSolverInput) -> None:
            raise CaptchaSolverException("Test error")
    return CaptchaSolverPortImpl()

class TestCaptchaSolverPort:
    def test_if_raises_captcha_solver_exception_if_solve_captcha_raises_exception(
        self,
        captcha_solver_port
    ):
        """
        Test if the CaptchaSolverPort raises a CaptchaSolverException if the solve_captcha method raises an exception.
        """
        with pytest.raises(CaptchaSolverException):
            captcha_solver_port.run(
                input=CaptchaSolverInput(
                    img_webelement=MagicMock(spec=WebElement), 
                    input_webelement=MagicMock(spec=WebElement)
                )
            )