from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.selenium.certidao_delmiro.pages import *

class DocumentDelmiroDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
    ):
        if not isinstance(consulta_page, ConsultaPage):
            raise ValueError("consulta_page must be a ConsultaPage")

        if not isinstance(download_page, DownloadPage):
            raise ValueError("download_page must be a DownloadPage")

        self.consulta_page = consulta_page
        self.download_page = download_page

    def get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        """
        Downloads the document by running the consulta page and the download page.

        :param input: The input of the document downloader.
        :type input: DocumentDownloaderInput
        :return: The document downloader output.
        :rtype: DocumentDownloaderOutput
        """
        if not isinstance(input, DocumentDownloaderInput):
            raise ValueError("input must be a DocumentDownloaderInput")

        self.consulta_page.run(cnpj=input.cnpj)
        document_extracted, base64_pdf = self.download_page.run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf
        )