from automacao_certificados.selenium_automations.adapters.api_requester.alagoas_api_requester import AlagoasAPIRequester
from automacao_certificados.selenium_automations.adapters.extractors.certificado_alagoas_extractor import CertificadoAlagoasExtractor
from automacao_certificados.selenium_automations.core.models import dto_document

from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort

from typing import Tuple

class DocumentAlagoasDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        api_requester: AlagoasAPIRequester,
    ):
        self.api_requester = api_requester

    def get_document(
        self,
        cnpj: str
    ) -> Tuple[dto_document.DocumentExtracted, str]:
        base64_pdf = self.api_requester.get_certificado(cnpj=cnpj)
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).run()
        return document_extracted, base64_pdf