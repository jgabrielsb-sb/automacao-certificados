from pydantic import BaseModel

from datetime import date

from automacao_certificados.selenium_automations.core.models import (
    dto_supplier
)

class DocumentExtracted(BaseModel):
    supplier: dto_supplier.Supplier
    document_type: str
    expiration_date: date

class Document(BaseModel):
    supplier_id: int
    document_type_id: str
    identifier: str
    expiration_date: date

class DocumentCreate(Document):
    pass

class DocumentResponse(Document):
    id: int
