from automacao_certificados.selenium_automations.adapters.document_downloader.document_maceio_downloader import DocumentMaceioDownloader
from automacao_certificados.selenium_automations.core.models import *

import pytest

from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import DownloadPage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestDocumentMaceioDownloader:
    @pytest.fixture
    def driver(self):
        return webdriver.Chrome()

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )

    def test_if_raises_value_error_if_cnpj_is_not_a_number(
        self,
        download_page: DownloadPage
    ):
        with pytest.raises(ValueError) as e:
            DocumentMaceioDownloader(
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="wrong_cnpj"))

        assert "cnpj must be a number" in str(e.value)

        

    def test_if_raises_download_certidao_estadual_al_exception_if_cnpj_has_less_than_14_digits(
        self,
        download_page: DownloadPage
    ):
        with pytest.raises(ValueError) as e:
            DocumentMaceioDownloader(
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="123"))

        assert "cnpj must have 14 digits" in str(e.value)


class TestHeadlessFalseCases:
    @pytest.fixture
    def driver(self):
        return webdriver.Chrome()

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )
    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self, download_page: DownloadPage):
        output = DocumentMaceioDownloader(
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="32652832000189"))

        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)

class TestHeadlessTrueCases:
    @pytest.fixture
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=true')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage") # important in Docker
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self, download_page: DownloadPage):
        output = DocumentMaceioDownloader(
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="32652832000189"))

        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
