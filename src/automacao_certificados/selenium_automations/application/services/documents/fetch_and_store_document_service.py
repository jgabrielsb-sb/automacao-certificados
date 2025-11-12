
from pydantic import BaseModel

import base64

from automacao_certificados.selenium_automations.core.interfaces import (
    DocumentAcquisitionPort, DocumentRequest, DocumentResult,
    DocumentPersistancePort, DocumentPersist, DocumentPersistResult
)

from automacao_certificados.selenium_automations.core.interfaces.document_persistance import DocumentPersistancePort
from automacao_certificados.selenium_automations.utils.utils import validate_document_file

class FetchAndStoreResult(BaseModel):
    document_request: DocumentRequest
    document_result: DocumentResult
    document_persist_result: DocumentPersistResult

class FetchAndStoreDocumentService:
    def __init__(
        self,
        acquisition: DocumentAcquisitionPort,
        persistence: DocumentPersistancePort,
    ):
        if not isinstance(acquisition, DocumentAcquisitionPort):
            raise ValueError("acquisition must be a DocumentAcquisitionPort")
        
        if not isinstance(persistence, DocumentPersistancePort):
            raise ValueError("persistence must be a DocumentPeristencePort")

        self._acquisition = acquisition
        self._persistence = persistence

    def execute(
        self,
        req: DocumentRequest
    ):
        # use acquisition port to get the document
        document_result = self._acquisition.acquire(req)

        # validate result
        if not isinstance(document_result, DocumentResult):
            raise ValueError("document_result must be a DocumentResult")

        # validate if the document is a valid pdf file
        validate_document_file(document_result.base64_pdf)

        document_persist = DocumentPersist(
            document_extracted=document_result.document_extracted,
            base64_pdf=document_result.base64_pdf
        )

        # use persistence port to save the document
        document_persist_result = self._persistence.save(document_result)

        return FetchAndStoreResult(
            document_request=req,
            document_result=document_result,
            document_persist_result=document_persist_result
        )



        
        