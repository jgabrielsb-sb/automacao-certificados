from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class CaptchaSolverPort(ABC):
    """
    Interface responsible for defining the contract for captcha solvers.
    """
    @abstractmethod
    def solve_captcha(self, input: CaptchaSolverInput) -> None:
        """
        Solves the captcha.
        
        :param input: the input of the captcha solver.
        :type input: CaptchaSolverInput
        :return: None
        :rtype: None
        """
        pass

    def run(self, input: CaptchaSolverInput) -> None:
        """
        Runs the captcha solver.
        
        :param input: the input of the captcha solver.
        :type input: CaptchaSolverInput
        :return: None
        :rtype: None
        """
        try:
            return self.solve_captcha(input)
        except Exception as e:
            raise CaptchaSolverException(e)