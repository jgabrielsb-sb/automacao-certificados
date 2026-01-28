from automacao_certificados.selenium_automations.adapters import DocumentPenedoDownloader

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_penedo.pages import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.config import settings

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from automacao_certificados.selenium_automations.adapters.image_processor.groq_image_processor import GroqImageProcessor
from automacao_certificados.selenium_automations.core.interfaces import ImageProcessorPort
from automacao_certificados.selenium_automations.core.models.interfaces.dto_image_processor import ImageProcessorInput, ImageProcessorOutput
from groq import Groq

import os


class MockImageProcessor(ImageProcessorPort):
    """Mock image processor for validation tests that don't need real captcha solving."""
    def get_text(self, input: ImageProcessorInput) -> ImageProcessorOutput:
        return ImageProcessorOutput(text="MOCK")


class TestDocumentPenedoDownloader:
    @pytest.fixture
    def driver(self):
        return webdriver.Chrome()

    @pytest.fixture
    def image_processor(self):
        # Use mock for validation tests - they don't actually run the consulta page
        return MockImageProcessor()

    @pytest.fixture
    def consulta_page(self, driver, image_processor):
        return ConsultaPage(
            driver=driver,
            image_processor=image_processor,
        )

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )
   
    def test_download_certificado_with_cnpj_with_less_than_14_digits(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            DocumentPenedoDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="2181000141"))
        assert "cnpj must have 14 digits" in str(e.value)
        
    def test_download_certificado_with_cnpj_with_more_than_14_digits(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            DocumentPenedoDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="2181123450001411223"))
        assert "cnpj must have 14 digits" in str(e.value)


class TestHeadlessFalseCases:
    @pytest.fixture
    def driver(self):
        from automacao_certificados.selenium_automations.infra.webdriver.global_webdriver import get_global_webdriver
        return get_global_webdriver()


    @pytest.fixture
    def image_processor(self):
        groq_api_key = settings.groq_api_key
        groq_client = Groq(api_key=groq_api_key)
        return GroqImageProcessor(client=groq_client)

    @pytest.fixture
    def consulta_page(self, driver, image_processor):
        return ConsultaPage(
            driver=driver,
            image_processor=image_processor,
        )

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )

    @pytest.mark.selenium_workflow_tests
    def test_download_certificado_penedo(self, consulta_page, download_page):
        output = DocumentPenedoDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="12243697000100"))

        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)


class TestHeadlessTrueCases:
    @pytest.fixture
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=true')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # important in Docker
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    @pytest.fixture
    def image_processor(self):
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            pytest.skip("GROQ_API_KEY environment variable not set")
        groq_client = Groq(api_key=groq_api_key)
        return GroqImageProcessor(client=groq_client)

    @pytest.fixture
    def consulta_page(self, driver, image_processor):
        return ConsultaPage(
            driver=driver,
            image_processor=image_processor,
        )

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )

    @pytest.mark.selenium_workflow_tests
    def test_download_certificado_penedo(self, consulta_page, download_page):
        output = DocumentPenedoDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="12243697000100"))

        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
