from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.core.models import *

from selenium.webdriver.chrome.webdriver import WebDriver

from typing import Tuple

class DocumentMaceioDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        download_page: DownloadPage
    ):
        """
        The document maceio downloader is an implementation of the document downloader port 
        that uses a download page to download the document.
        """
        if not isinstance(download_page, DownloadPage):
            raise ValueError("download_page must be a DownloadPage")

        self.download_page = download_page

    def get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        """
        Downloads the document by running the download page.

        :param input: The input of the document downloader.
        :type input: DocumentDownloaderInput
        :return: The document downloader output.
        :rtype: DocumentDownloaderOutput
        """
        if not isinstance(input, DocumentDownloaderInput):
            raise ValueError("input must be a DocumentDownloaderInput")

        document_extracted, base64_pdf = self.download_page.run(cnpj=input.cnpj)
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf
        )