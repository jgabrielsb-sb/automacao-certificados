from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document

from selenium.webdriver.chrome.webdriver import WebDriver

from typing import Tuple

class DocumentMaceioDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        download_page: DownloadPage
    ):
        self.download_page = download_page

    def get_document(self, cnpj: str) -> Tuple[dto_document.DocumentExtracted, str]:
        return self.download_page.run(cnpj=cnpj)