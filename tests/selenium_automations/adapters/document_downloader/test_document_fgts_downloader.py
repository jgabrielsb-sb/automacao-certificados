from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
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

    def atest_if_raises_value_error_if_incorrect_cnpj(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            DocumentFGTSDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="wrong_cnpj"))

        assert "cnpj must be a number" in str(e.value)

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self, consulta_page, download_page):
        output = DocumentFGTSDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="15401595000164"))

        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
