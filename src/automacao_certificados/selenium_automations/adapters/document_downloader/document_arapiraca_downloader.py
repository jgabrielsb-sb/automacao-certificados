from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_arapiraca.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort
from pathlib import Path

class DocumentArapiracaDownloader(DocumentDownloaderPort):
    def __init__(   
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        self.consulta_page = consulta_page
        self.download_page = download_page

    def get_document(self, cnpj: str) -> tuple[dto_document.DocumentExtracted, str]:
        self.consulta_page.run(cnpj=cnpj)
        return self.download_page.run()