from automacao_certificados.selenium_automations.core.interfaces.selenium_downloader import SeleniumDocumentDownloaderPort
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *

from typing import Tuple
from selenium.webdriver.chrome.webdriver import WebDriver

class DocumentFGTSDownloader(SeleniumDocumentDownloaderPort):
    def __init__(
        self,
        driver: WebDriver,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        super().__init__(driver)
        self.consulta_page = consulta_page
        self.download_page = download_page

    def get_document(self, cnpj: str) -> Tuple[dto_document.DocumentExtracted, str]:
        self.consulta_page.run(state_value="AL", tipo_inscricao_value="CNPJ", inscricao_value=cnpj)
        return self.download_page.run()