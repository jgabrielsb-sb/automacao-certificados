

from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import (
    LoggingRegisterInput
)

from automacao_certificados.selenium_automations.core.exceptions import (
    LoggingRegisterException
)

class LoggingRegister(ABC):
    """
    The base interface for registering logs of the system.
    """

    @abstractmethod
    def register(self, input: LoggingRegisterInput):
        """
        Must be implemented by child classes

        :param input: the log to be registered
        :type input: LoggingRegisterInput

        :return: none
        :rtype: None
        """
        pass

    def run(self, input: LoggingRegisterInput):
        if not isinstance(input, LoggingRegisterInput):
            raise ValueError("input must be a LoggingRegisterInput")
            
        try:
            self.register(input)
        except Exception as e:
            raise LoggingRegisterException(e)
