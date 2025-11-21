from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import MunicipioEnum
from automacao_certificados.selenium_automations.utils import validate_cnpj
from automacao_certificados.selenium_automations.core.exceptions import *

class MunicipioGetterPort(ABC):
    """
    Interface responsible for getting the municipality by cnpj.
    """
    @abstractmethod
    def _get_municipio_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the municipality by cnpj.
        Args:
            cnpj: the cnpj of the supplier.
        Returns:
            The municipality enum.
        """
        pass

    def run(self, cnpj: str) -> str:
        """
        Runs the municipality getter.
        Args:
            cnpj: the cnpj of the supplier.
        Returns:
            The municipality enum.
        """
        validate_cnpj(cnpj)
        try:
            municipio = self._get_municipio_by_cnpj(cnpj)
            return municipio
        except Exception as e:
            raise MunicipioGetterException(e)
