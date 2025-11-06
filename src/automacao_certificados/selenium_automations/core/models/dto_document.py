from pydantic import BaseModel

from datetime import date

from typing import Optional

from automacao_certificados.selenium_automations.core.models import (
    dto_supplier
)

class DocumentExtracted(BaseModel):
    supplier: dto_supplier.Supplier
    document_type: str
    identifier: str
    expiration_date: date

class Document(BaseModel):
    supplier_id: int
    document_type_id: int
    identifier: str
    expiration_date: date
    base64_pdf: str

class DocumentCreate(Document):
    pass

class DocumentResponse(Document):
    id: int

class DocumentFilter(BaseModel):
    supplier_id: Optional[int] = None
    document_type_id: Optional[int] = None
    identifier: Optional[str] = None
    expiration_date: Optional[date] = None
    limit: int = 10