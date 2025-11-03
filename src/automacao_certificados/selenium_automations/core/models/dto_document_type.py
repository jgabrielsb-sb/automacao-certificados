from pydantic import BaseModel

from typing import Optional

class DocumentType(BaseModel):
    name: str

class DocumentTypeCreate(DocumentType):
    pass

class DocumentTypeResponse(DocumentType):
    id: int

class DocumentTypeFilter(BaseModel):
    name: Optional[str] = None