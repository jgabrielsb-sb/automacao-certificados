import pytest
from selenium import webdriver
from datetime import date

from automacao_certificados.selenium_automations.adapters.document_downloader import DocumentDelmiroDownloader
from automacao_certificados.selenium_automations.adapters.selenium.certidao_delmiro.pages import *

from automacao_certificados.selenium_automations.core.exceptions import DocumentDownloaderException
from automacao_certificados.selenium_automations.core.models import (
    DocumentDownloaderInput, 
    DocumentExtracted
)


@pytest.fixture
def driver():
    return webdriver.Chrome()

@pytest.fixture
def consulta_page(driver):
    return ConsultaPage(
        driver=driver,
    )

@pytest.fixture
def download_page(driver):
    return DownloadPage(
        driver=driver,
    )
class TestInitDocumentDelmiroDownloader:


    def test_if_raises_value_error_if_consulta_page_is_not_a_consulta_page(self, consulta_page, download_page):
        with pytest.raises(ValueError):
            DocumentDelmiroDownloader(
                consulta_page="not a consulta page",
                download_page=download_page,
            )

    def test_if_raises_value_error_if_download_page_is_not_a_download_page(self, consulta_page, download_page):
        with pytest.raises(ValueError):
            DocumentDelmiroDownloader(
                consulta_page=consulta_page,
                download_page="not a download page",
            )

class TestGetDocumentDocumentDelmiroDownloader:
    def test_if_raises_value_error_if_input_is_not_a_document_downloader_input(self, consulta_page, download_page):
        with pytest.raises(ValueError):
            DocumentDelmiroDownloader(
                consulta_page=consulta_page,
                download_page=download_page,
            ).get_document(input="not a document downloader input")

class TestRunDocumentDelmiroDownloader:
    def test_sucess_case_1(self, consulta_page, download_page):
        
        output =DocumentDelmiroDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="12517413000470"))
        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
        
        assert output.document_extracted.supplier.cnpj == "12.517.413/0004-70"
        assert output.document_extracted.document_type == "Certidão Negativa Municipal"
        assert isinstance(output.document_extracted.identifier, str)
        assert isinstance(output.document_extracted.expiration_date, date)

    def test_sucess_case_2(self, consulta_page, download_page):
        output =DocumentDelmiroDownloader(
            consulta_page=consulta_page,
            download_page=download_page,
        ).run(input=DocumentDownloaderInput(cnpj="17503314000100"))
        assert isinstance(output.document_extracted, DocumentExtracted)
        assert isinstance(output.base64_pdf, str)
        
        assert output.document_extracted.supplier.cnpj == "17.503.314/0001-00"
        assert output.document_extracted.document_type == "Certidão Negativa Municipal"
        assert isinstance(output.document_extracted.identifier, str)
        assert isinstance(output.document_extracted.expiration_date, date)