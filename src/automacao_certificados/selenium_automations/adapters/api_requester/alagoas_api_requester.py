
from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester
from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from automacao_certificados.selenium_automations.core.exceptions import *

from pydantic import BaseModel

from http import HTTPStatus
import base64

from automacao_certificados.selenium_automations.utils.utils import validate_cnpj


class CertificadoPostRequest(BaseModel):
    numeroDocumento: str
    tipoDocumento: str

DEFAULT_BASE_URL = "https://contribuinte.sefaz.al.gov.br"

class AlagoasAPIRequester:
    def __init__(
        self, 
        http: HttpClient,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.base_url = base_url
        self.http = http

    def get_certificado(
        self,
        cnpj: str
    ) -> str:
        """
        Get the certificado from the Alagoas API.
        Arguments:
            certificado_post_request: The request to get the certificado.
        Returns:
            The PDF certificado in base64 format.
        Raises:
            UnexpectedError: If an unexpected error occurs.
        """
        cnpj = validate_cnpj(cnpj=cnpj)
        
        url = f"{self.base_url}/certidao/sfz-certidao-api/api/public/emitirCertidao"
        response = self.http.post(url, json={
            'numeroDocumento': cnpj,
            'tipoDocumento': "CNPJ"
        })
        
        if response.status_code == HTTPStatus.OK:
            file = response.json().get('conteudo')
            if file:
                return file
            else:
                raise UnexpectedError(
                    route=url,
                    message=f"Unexpected error. The API Response does not have 'conteudo' key. API Response: {response.json()}",
                    status_code=response.status_code
                )
        
        elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            description = response.json().get('description')
            
            if 'CNPJ inválido' in description:
                custom_message = f"CNPJ is invalid or does not exist: {cnpj}. API Response: {response.json()}"
                raise InvalidCNPJException(
                    cnpj=cnpj,
                    custom_message=custom_message
                )

        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error: API Response: {response.json()}",
                status_code=response.status_code
            )