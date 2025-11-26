from automacao_certificados.selenium_automations.adapters import DocumentArapiracaDownloader

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_arapiraca.pages import *
from automacao_certificados.selenium_automations.core.exceptions import *

import pytest

from selenium.webdriver.chrome.webdriver import WebDriver

class TestDocumentArapiracaDownloader:
    @pytest.fixture
    def driver(self):
        return WebDriver()

    @pytest.fixture
    def consulta_page(self, driver):
        return ConsultaPage(
            driver=driver,
        )

    @pytest.fixture
    def download_page(self, driver):
        return DownloadPage(
            driver=driver,
        )
    
    @pytest.mark.selenium_workflow_tests
    def test_download_certificado_arapiraca(self, consulta_page, download_page):
        output = DocumentArapiracaDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="21818221000141"))

        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)

    @pytest.mark.selenium_workflow_tests
    def test_download_certificado_arapiraca_2(self, consulta_page, download_page):
        output = DocumentArapiracaDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="39549075000161"))

        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)

    def test_download_certificado_with_cnpj_with_less_than_14_digits(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            document_extracted, base64_pdf = DocumentArapiracaDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="2181000141"))
        assert "cnpj must have 14 digits" in str(e.value)
        
    def test_download_certificado_with_cnpj_with_more_than_14_digits(self, consulta_page, download_page):
        with pytest.raises(ValueError) as e:
            document_extracted, base64_pdf = DocumentArapiracaDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).run(input=DocumentDownloaderInput(cnpj="2181123450001411223"))
        assert "cnpj must have 14 digits" in str(e.value)
        
        
       
    