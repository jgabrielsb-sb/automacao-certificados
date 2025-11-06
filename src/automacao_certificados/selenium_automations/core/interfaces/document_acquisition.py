from typing import Protocol, runtime_checkable

from automacao_certificados.selenium_automations.core.models import dto_document
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    """
    Request model for document acquisition.
    """
    cnpj: str

class DocumentResult(BaseModel):
    """
    Result model for document acquisition.
    """
    document_extracted: dto_document.DocumentExtracted
    base64_pdf: str

@runtime_checkable
class DocumentAcquisitionPort(Protocol):
    def acquire(self, req: DocumentRequest) -> DocumentResult: ...