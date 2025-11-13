from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document

class CertificadoMaceioWorkflow:
    def __init__(
        self,
        download_page: DownloadPage,
        
    ):
        self.download_page = download_page

    def run(
        self,
        cnpj: str,
    ) -> tuple[dto_document.DocumentExtracted, str]:
        return self.download_page.run(cnpj=cnpj)