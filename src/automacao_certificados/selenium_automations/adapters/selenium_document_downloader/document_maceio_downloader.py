
from automacao_certificados.selenium_automations.core.interfaces import SeleniumDocumentDownloaderPort
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document

from typing import Tuple

class DocumentMaceioDownloader(SeleniumDocumentDownloaderPort):
    def __init__(
        self,
        driver,
        download_page: DownloadPage
    ):
        super().__init__(driver)
        self.download_page = download_page

    def get_document(self, cnpj: str) -> Tuple[dto_document.DocumentExtracted, str]:
        return self.download_page.run(cnpj=cnpj)