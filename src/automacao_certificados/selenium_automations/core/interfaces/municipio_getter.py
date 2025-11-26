from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.utils import validate_cnpj
from automacao_certificados.selenium_automations.core.exceptions import *

class MunicipioGetterPort(ABC):
    """
    Interface responsible for getting the municipality by cnpj.
    """
    @abstractmethod
    def get_municipio_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the municipality by cnpj.

        :param cnpj: the cnpj of the supplier.
        :type cnpj: str

        :return: the municipality name.
        :rtype: str
        """
        pass

    def run(self, cnpj: str) -> str:
        """
        Runs the municipality getter.

        :param cnpj: the cnpj of the supplier.
        :type cnpj: str
        :return: the municipality name.
        :rtype: str
        """
        validate_cnpj(cnpj)
        try:
            municipio = self.get_municipio_by_cnpj(cnpj)
            return municipio
        except Exception as e:
            raise MunicipioGetterException(e)
