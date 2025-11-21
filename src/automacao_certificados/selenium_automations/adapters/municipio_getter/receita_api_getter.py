from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.models import *

class ReceitaAPIMunicipioGetter(MunicipioGetterPort):
    def __init__(self, api_requester: ReceitaAPIRequester):
        self.api_requester = api_requester

    def _get_municipio_by_cnpj(self, cnpj: str) -> str:
        company = self.api_requester.get_company(cnpj=cnpj)
        municipio = company.END_MUNICIPIO
        return municipio
