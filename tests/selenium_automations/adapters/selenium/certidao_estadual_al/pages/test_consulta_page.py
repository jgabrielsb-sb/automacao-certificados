import pytest
from unittest.mock import Mock

from selenium.webdriver.chrome.webdriver import WebDriver

from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.pages import ConsultaPage

from automacao_certificados.selenium_automations.adapters.selenium.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import CaptchaSolverPort

@pytest.fixture
def consulta_page_instance():
    return ConsultaPage(
        driver=Mock(spec=WebDriver),
        captcha_solver=Mock(spec=CaptchaSolverPort)
    )


class TestConsultaPage:

    def test_if_insert_tipo_inscricao_value_executor_raises_invalid_tipo_inscricao_exception(
        self,
        consulta_page_instance: ConsultaPage,
    ):
        with pytest.raises(InvalidTipoInscricaoException):
            consulta_page_instance.insert_tipo_inscricao_value_executor("INVALID_TYPE").run()

    def test_if_insert_estado_value_raises_invalid_estado_exception(
        self,
        consulta_page_instance: ConsultaPage,
    ):
        with pytest.raises(InvalidEstadoException):
            consulta_page_instance.insert_estado_value_executor("INVALID_STATE").run()