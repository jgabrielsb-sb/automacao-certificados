from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *
from automacao_certificados.config import settings

from groq import Groq

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestDocumentFGTSDownloader:
    @pytest.fixture
    def driver(self):
        return webdriver.Chrome()

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


class TestHeadlessFalseCases:
    @pytest.fixture
    def driver(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless=false')
        return webdriver.Chrome()

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

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self, consulta_page, download_page):
        output = DocumentFGTSDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="15401595000164"))

        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)

class TestHeadlessTrueCases:
    @pytest.fixture
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage") # important in Docker
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

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

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self, consulta_page, download_page):
        output = DocumentFGTSDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="15401595000164"))

        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
