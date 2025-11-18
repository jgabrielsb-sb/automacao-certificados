from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester
from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from .exceptions import *

from pydantic import BaseModel

from http import HTTPStatus

from enum import Enum

BASE_URL = 'https://ppe.hml.sebrae.al'

class DocumentTypeEnum(Enum):
    CERTIDAO_NEGATIVA_FGTS = 'Certidão Negativa FGTS'
    CERTIDAO_NEGATIVA_FEDERAL = 'Certidão Negativa Federal'
    CERTIDAO_NEGATIVA_MUNICIPAL = 'Certidão Negativa Municipal'
    CERTIDAO_NEGATIVA_ESTADUAL = 'Certidão Negativa Estadual'

class CertificateToDownload(BaseModel):
    cnpj: str
    certificates: list[DocumentTypeEnum]

class PPEAPIRequester:
    def __init__(
        self,
        http: HttpClient,
        api_key: str,
        base_url: str = BASE_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.http = http

    def get_certificates_to_download(
        self,
    ) -> list[CertificateToDownload]:
        url = f"{self.base_url}/api/company/certificate/"
        
        response = self.http.get(url, headers={
            'X-Api-Key': f'{self.api_key}'
        })

        if response.status_code == HTTPStatus.OK:
            response_data = response.json()
            certificates_to_download = [
                CertificateToDownload(
                    cnpj=item['cnpj'], 
                    certificates=[
                        DocumentTypeEnum(certificate) for certificate in item['certificates']
                    ]
                ) for item in response_data]
            return certificates_to_download
        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error. The API Response down: {response_data}",
                status_code=response.status_code
            )

        

    