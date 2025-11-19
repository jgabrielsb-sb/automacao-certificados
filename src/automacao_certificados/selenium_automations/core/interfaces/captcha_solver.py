from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class CaptchaSolverPort(ABC):
    """
    Interface responsible for solving the captcha.
    """
    @abstractmethod
    def _solve_captcha(self, input: CaptchaSolverInput) -> None:
        """
        Method to be implemented by child classes.
        """
        pass

    def run(self, input: CaptchaSolverInput) -> None:
        try:
            return self._solve_captcha(input)
        except Exception as e:
            raise CaptchaSolverException(e)