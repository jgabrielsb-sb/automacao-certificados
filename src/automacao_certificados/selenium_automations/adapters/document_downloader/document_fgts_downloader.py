from automacao_certificados.selenium_automations.core.interfaces.document_downloader import DocumentDownloaderPort
from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document

from typing import Tuple

class DocumentFGTSDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        self.consulta_page = consulta_page
        self.download_page = download_page

    def get_document(self, cnpj: str) -> Tuple[dto_document.DocumentExtracted, str]:
        self.consulta_page.run(state_value="AL", tipo_inscricao_value="CNPJ", inscricao_value=cnpj)
        return self.download_page.run()