import pytest
from unittest.mock import MagicMock
from automacao_certificados.selenium_automations.adapters.municipio_getter.receita_api_getter import ReceitaAPIMunicipioGetter
from automacao_certificados.selenium_automations.infra.api_requester import ReceitaAPIRequester
from automacao_certificados.selenium_automations.adapters import HttpxClient
from automacao_certificados.selenium_automations.core.models import *

class TestReceitaAPIMunicipioGetter:
    def test_get_municipio_by_cnpj(self):
        api_requester = MagicMock(spec=ReceitaAPIRequester)
        output = ReceitaAPIGetCompanyResponse(END_MUNICIPIO="ARAPIRACA")
        api_requester.get_company.return_value = output
        
        receita_api_municipio_getter = ReceitaAPIMunicipioGetter(api_requester=api_requester)
        municipio = receita_api_municipio_getter.get_municipio_by_cnpj(cnpj="1234567890")
        assert municipio == "ARAPIRACA"

        
        
