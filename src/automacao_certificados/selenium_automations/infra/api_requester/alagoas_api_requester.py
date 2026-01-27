
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

#### DEVERIA SER INFRA

class AlagoasAPIRequester:
    def __init__(
        self, 
        http: HttpClient,
        base_url: str = DEFAULT_BASE_URL,
    ):
        """
        The alagoas api requester is responsible for making requests to the Alagoas Certidão API.
        """

        self.base_url = base_url
        self.http = http

    def get_certificado(
        self,
        cnpj: str
    ) -> str:
        """
        Get the certificado from the Alagoas Certidão API.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The PDF certificado in base64 format.
        :rtype: str
        :raises UnexpectedError: If an unexpected error occurs.
        :raises InvalidCNPJException: If the cnpj is invalid or does not exist.
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
            
            if description and'CNPJ inválido' in description:
                custom_message = f"CNPJ is invalid or does not exist: {cnpj}. API Response: {response.json()}"
                raise InvalidCNPJException(
                    cnpj=cnpj,
                    custom_message=custom_message
                )
            elif description and 'Não foi possível emitir' in description:
                raise SucessoComRessalvasException(
                    message=f"Could not generate PDF caused by CNPJ issues: API Response: {response.json()}"
                )
            else:
                raise UnexpectedError(
                    route=url,
                    message=f"Unexpected error. API Response: {response.json()}",
                    status_code=response.status_code
                )
        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error: API Response: {response.json()}",
                status_code=response.status_code
            )