from pydantic import BaseModel

from typing import Protocol, runtime_checkable

from automacao_certificados.selenium_automations.core.models import dto_document

class SeleniumWorkflowInput(BaseModel):
    supplier_cnpj: str

class SeleniumWorkflowOutput(BaseModel):
    document: dto_document.DocumentExtracted
    base64_pdf: str


@runtime_checkable
class SeleniumWorkflowPort(Protocol):
    def get_document(self, input: SeleniumWorkflowInput) -> SeleniumWorkflowOutput: ... 

