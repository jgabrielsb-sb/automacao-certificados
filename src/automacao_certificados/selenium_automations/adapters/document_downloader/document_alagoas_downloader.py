from automacao_certificados.selenium_automations.adapters.extractors.certificado_alagoas_extractor import CertificadoAlagoasExtractor
from automacao_certificados.selenium_automations.core.exceptions.adapters.api_requester_exceptions import (
    APIRequesterException, 
    SucessoComRessalvasException
)
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester, PPEAPIRequester
from automacao_certificados.selenium_automations.core.interfaces import DocumentDownloaderPort

from typing import Tuple

class DocumentAlagoasDownloader(DocumentDownloaderPort):
    def __init__(
        self,
        api_requester: AlagoasAPIRequester,
        ppe_api_requester: PPEAPIRequester,
    ):    
        """
        The document alagoas downloader is an implementation of the document downloader port 
        that uses an alagoas api requester to download the document.
        """

        if not isinstance(api_requester, AlagoasAPIRequester):
            raise ValueError("api_requester must be a AlagoasAPIRequester")
        if not isinstance(ppe_api_requester, PPEAPIRequester):
            raise ValueError("ppe_api_requester must be a PPEAPIRequester")

        self.api_requester = api_requester
        self.ppe_api_requester = ppe_api_requester
        
    def _block_on_ppe(self, *, cnpj: str) -> str:
        """
        Blocks the search for the certificate on the PPE API.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: A message indicating that the request to block the search for the certificate was made successfully or an error message.
        :rtype: str
        """
        try:
            response = self.ppe_api_requester.block_certificate(
                cnpj,
                DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL,
            )
            return (
                "OBS: a request to block the search for the certificate was made successfully. "
                f"The response was: {response}"
            )
        except APIRequesterException as e:
            return (
                "OBS: the request to block the search for the certificate got an error: "
                f"{str(e)}"
            )

    def _get_base64_or_raise_ressalvas(self, *, cnpj: str) -> str:
        """
        Single source of truth for:
        - calling Direct Data
        - if SucessoComRessalvasException happens, attempt PPE block (best-effort)
        - re-raise SucessoComRessalvasException with enriched message
        """
        try:
            return self.api_requester.get_certificado(cnpj=cnpj)
        except SucessoComRessalvasException as e:
            note = self._block_on_ppe(cnpj=cnpj)
            raise SucessoComRessalvasException(message=f"{e.message}. {note}") from e

    def get_certificado_base64(self, cnpj: str) -> str:
        if not isinstance(cnpj, str):
            raise ValueError("cnpj must be a string")
            
        return self._get_base64_or_raise_ressalvas(cnpj=cnpj)

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

        base64_pdf = self._get_base64_or_raise_ressalvas(cnpj=input.cnpj)
        document_extracted = CertificadoAlagoasExtractor(base64_pdf=base64_pdf).run()
        return DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf=base64_pdf,
        )