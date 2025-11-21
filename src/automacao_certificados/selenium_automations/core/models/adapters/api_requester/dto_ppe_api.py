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
    certificates: list[DocumentTypeEnum]

class PPEGetCertificatesToDownloadResponse(BaseModel):
    certificates: list[CertificateToDownload]

class PPEPostCertificateRequest(BaseModel):
    document: str # cnpj (only numbers)
    certificate: DocumentTypeEnum 
    number: str 
    validity: date 
    pdf: str #base64 pdf string

    # model_config = ConfigDict(
    #     ser_json_timedelta = True,
    #     ser_json_bytes = True,
    #     ser_json = True
    # )





