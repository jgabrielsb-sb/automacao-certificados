from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.infra.api_requester import ReceitaAPIRequester

class ReceitaAPIMunicipioGetter(MunicipioGetterPort):
    def __init__(self, api_requester: ReceitaAPIRequester):
        """
        The receita api municipio getter is an implementation of the municipio getter port 
        that uses the receita api to get the municipality by cnpj.
        """
        if not isinstance(api_requester, ReceitaAPIRequester):
            raise ValueError("api_requester must be a ReceitaAPIRequester")

        super().__init__()

        self.api_requester = api_requester

    def get_municipio_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the municipality by cnpj using the receita api.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The municipality name.
        :rtype: str
        """
        company = self.api_requester.get_company(cnpj=cnpj)
        municipio = company.END_MUNICIPIO
        return municipio
