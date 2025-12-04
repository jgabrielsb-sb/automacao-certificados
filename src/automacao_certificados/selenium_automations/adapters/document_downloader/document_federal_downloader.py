
from automacao_certificados.selenium_automations.adapters.extractors.certificado_federal_extractor import CertificadoFederalExtractor
from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort
from automacao_certificados.selenium_automations.core.models.interfaces.dto_document_downloader import DocumentDownloaderInput, DocumentDownloaderOutput
from automacao_certificados.selenium_automations.infra.api_requester.direct_data_api_requester import DirectDataAPIRequester



class DocumentFederalDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        api_requester: DirectDataAPIRequester,
    ):
        if not isinstance(api_requester, DirectDataAPIRequester):
            raise ValueError("api_requester must be a DirectDataAPIRequester")

        self.api_requester = api_requester

    def get_document(
        self,
        input: DocumentDownloaderInput
    ) -> DocumentDownloaderOutput:
        if not isinstance(input, DocumentDownloaderInput):
            raise ValueError("input must be a DocumentDownloaderInput")

        base64_pdf = self.api_requester.get_certificado_base64(cnpj=input.cnpj)
        document_extracted = CertificadoFederalExtractor(base64_pdf=base64_pdf).run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf,
        )