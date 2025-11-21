from pydoc import Doc
from pydantic import BaseModel, ConfigDict

from enum import Enum

from datetime import date

class DocumentTypeEnum(Enum):
    CERTIDAO_NEGATIVA_FGTS = 'Certidão Negativa FGTS'
    CERTIDAO_NEGATIVA_FEDERAL = 'Certidão Negativa Federal'
    CERTIDAO_NEGATIVA_MUNICIPAL = 'Certidão Negativa Municipal'
    CERTIDAO_NEGATIVA_ESTADUAL = 'Certidão Negativa Estadual'

class CertificateToDownload(BaseModel):
    cnpj: str
    document_type: DocumentTypeEnum

class PPEPostCertificateRequest(BaseModel):
    document: str # cnpj (only numbers)
    certificate: DocumentTypeEnum 
    number: str 
    validity: date 
    pdf: str #base64 pdf string







