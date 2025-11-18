from automacao_certificados.selenium_automations.adapters import (
    ImageCaptchaSolver, 
    GroqImageProcessor, 
    SeleniumCaptchaGateway,
    DocumentFGTSDownloader,
)
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters.selenium.exceptions import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *
from automacao_certificados.config import settings

from groq import Groq

import pytest

from selenium.webdriver.chrome.webdriver import WebDriver

class TestDocumentFGTSDownloader:
    @pytest.fixture
    def driver(self):
        return WebDriver()

    @pytest.fixture
    def consulta_page(self, driver):
        return ConsultaPage(
            driver=driver,
            captcha_solver=ImageCaptchaSolver(
                image_processor=GroqImageProcessor(
                    client=Groq(api_key=settings.groq_api_key),
                ),
                captcha_gateway=SeleniumCaptchaGateway(
                    webdriver=driver,
                ),
            ),
        )

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )

    def test_if_raises_value_error_if_incorrect_cnpj(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            DocumentFGTSDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run("wrong_cnpj")

        assert "cnpj must be a number" in str(e.value)

    def test_sucess_case(self,consulta_page, download_page):
        document_extracted, base64_pdf = DocumentFGTSDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run("15401595000164")

        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)
