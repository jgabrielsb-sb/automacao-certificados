import pytest

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

@pytest.fixture
def municipio_getter_port():
    class MunicipioGetterPortImpl(MunicipioGetterPort):
        def get_municipio_by_cnpj(self, cnpj: str) -> str:
            return "ARAPIRACA"
    
    return MunicipioGetterPortImpl()


class TestMunicipioGetter:
    def testget_municipio_by_cnpj(
        self,
        municipio_getter_port: MunicipioGetterPort
    ):
        municipio = municipio_getter_port.get_municipio_by_cnpj("1234567890")
        assert municipio == "ARAPIRACA"

    def test_if_run_is_being_wrapped_into_municipio_getter_exception(
        self,
        monkeypatch,
        municipio_getter_port: MunicipioGetterPort
    ):
        def fakeget_municipio_by_cnpj(cnpj: str) -> str:
            raise Exception('test exception')

        monkeypatch.setattr(
            municipio_getter_port,
            "get_municipio_by_cnpj",
            fakeget_municipio_by_cnpj
        )

        with pytest.raises(MunicipioGetterException):
            municipio_getter_port.run("12345678912345")

    def test_run(
        self,
        municipio_getter_port: MunicipioGetterPort
    ):
        municipio = municipio_getter_port.run("12345678912345")
        assert municipio == "ARAPIRACA"