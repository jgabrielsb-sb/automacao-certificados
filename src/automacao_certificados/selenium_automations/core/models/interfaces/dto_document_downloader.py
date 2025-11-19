from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import dto_document

class DocumentDownloaderInput(BaseModel):
    cnpj: str

class DocumentDownloaderOutput(BaseModel):
    document_extracted: dto_document.DocumentExtracted
    base64_pdf: str