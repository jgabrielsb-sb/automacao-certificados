from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.utils import validate_cnpj
from automacao_certificados.selenium_automations.core.exceptions import *

class EstadoGetterPort(ABC):
    """
    Interface responsible for getting the estado by cnpj.
    """
    @abstractmethod
    def get_estado_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the estado by cnpj.

        :param cnpj: the cnpj of the supplier.
        :type cnpj: str

        :return: the estado name.
        :rtype: str
        """
        pass

    def run(self, cnpj: str) -> str:
        """
        Runs the estado getter.

        :param cnpj: the cnpj of the supplier.
        :type cnpj: str
        :return: the estado name.
        :rtype: str
        """
        validate_cnpj(cnpj)
        try:
            estado = self.get_estado_by_cnpj(cnpj)
            return estado
        except Exception as e:
            raise EstadoGetterException(e)
