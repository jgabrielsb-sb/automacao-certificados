from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.infra.api_requester import ReceitaAPIRequester

class ReceitaAPIEstadoGetter(EstadoGetterPort):
    def __init__(self, api_requester: ReceitaAPIRequester):
        """
        The receita api estado getter is an implementation of the estado getter port 
        that uses the receita api to get the estado by cnpj.
        """
        if not isinstance(api_requester, ReceitaAPIRequester):
            raise ValueError("api_requester must be a ReceitaAPIRequester")

        super().__init__()

        self.api_requester = api_requester

    def get_estado_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the estado by cnpj using the receita api.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The estado name.
        :rtype: str
        """
        company = self.api_requester.get_company(cnpj=cnpj)
        estado = company.END_UF
        return estado
