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
        self.api_requester = api_requester

    def _get_document(
        self,
        input: DocumentDownloaderInput
    ) -> DocumentDownloaderOutput:
        base64_pdf = self.api_requester.get_certificado(cnpj=input.cnpj)
        document_extracted = CertificadoAlagoasExtractor(base64_pdf=base64_pdf).run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf,
        )