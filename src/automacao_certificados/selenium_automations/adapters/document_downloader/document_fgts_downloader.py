from automacao_certificados.selenium_automations.core.interfaces.document_downloader import DocumentDownloaderPort
from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *
from automacao_certificados.selenium_automations.core.models import *

class DocumentFGTSDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        self.consulta_page = consulta_page
        self.download_page = download_page

    def _get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        self.consulta_page.run(state_value="AL", tipo_inscricao_value="CNPJ", inscricao_value=input.cnpj)
        document_extracted, base64_pdf = self.download_page.run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf
        )