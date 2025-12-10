from automacao_certificados.selenium_automations.adapters import DocumentArapiracaDownloader

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_arapiraca.pages import *
from automacao_certificados.selenium_automations.core.exceptions import *

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestDocumentArapiracaDownloader:
    @pytest.fixture
    def driver(self):
        return webdriver.Chrome()

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

class TestHeadlessFalseCases:
    @pytest.fixture
    def driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=false')
        return webdriver.Chrome(options=options)

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
        
        
       
    