from automacao_certificados.selenium_automations.adapters import DocumentMaceioDownloader
from automacao_certificados.selenium_automations.core.models import dto_document

import pytest

from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import DownloadPage

from selenium.webdriver.chrome.webdriver import WebDriver

class TestDocumentMaceioDownloader:
    @pytest.fixture
    def driver(self):
        return WebDriver()

    @pytest.fixture
    def download_page(self, driver: WebDriver):
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
            ).run("wrong_cnpj")

        assert "cnpj must be a number" in str(e.value)

        

    def test_if_raises_download_certidao_estadual_al_exception_if_cnpj_has_less_than_14_digits(
        self,
        download_page: DownloadPage
    ):
        with pytest.raises(ValueError) as e:
            DocumentMaceioDownloader(
                download_page=download_page,
            ).run("123")

        assert "cnpj must have 14 digits" in str(e.value)

    def test_sucess_case(self, download_page: DownloadPage):
        document_extracted, base64_pdf = DocumentMaceioDownloader(
            download_page=download_page,
        ).run(cnpj="32652832000189")

        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)