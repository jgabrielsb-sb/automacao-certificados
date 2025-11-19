from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import dto_document

class DocumentPersistanceInput(BaseModel):
    document_extracted: dto_document.DocumentExtracted
    base64_pdf: str

class DocumentPersistanceOutput(BaseModel):
    result: dict | str # should be passed the response of the api, for example.


