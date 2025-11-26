from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester
from automacao_certificados.selenium_automations.adapters.extractors.certificado_alagoas_extractor import CertificadoAlagoasExtractor
from automacao_certificados.selenium_automations.core.models import *

from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort

from typing import Tuple

class DocumentAlagoasDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        api_requester: AlagoasAPIRequester,
    ):
        """
        The document alagoas downloader is an implementation of the document downloader port 
        that uses an alagoas api requester to download the document.
        """
        if not isinstance(api_requester, AlagoasAPIRequester):
            raise ValueError("api_requester must be a AlagoasAPIRequester")

        self.api_requester = api_requester

    def get_document(
        self,
        input: DocumentDownloaderInput
    ) -> DocumentDownloaderOutput:
        """
        Downloads the document by getting the base64 pdf from the alagoas api requester 
        and extracting the document using the certificado alagoas extractor.

        :param input: The input of the document downloader.
        :type input: DocumentDownloaderInput
        :return: The document downloader output.
        :rtype: DocumentDownloaderOutput
        """
        if not isinstance(input, DocumentDownloaderInput):
            raise ValueError("input must be a DocumentDownloaderInput")

        base64_pdf = self.api_requester.get_certificado(cnpj=input.cnpj)
        document_extracted = CertificadoAlagoasExtractor(base64_pdf=base64_pdf).run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf,
        )