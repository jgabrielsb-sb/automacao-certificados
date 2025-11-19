from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_arapiraca.pages import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort

class DocumentArapiracaDownloader(DocumentDownloaderPort):
    def __init__(   
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        self.consulta_page = consulta_page
        self.download_page = download_page

    def _get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        self.consulta_page.run(cnpj=input.cnpj)
        document_extracted, base64_pdf = self.download_page.run()
        print(document_extracted, base64_pdf)
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf
        )