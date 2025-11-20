from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

from http import HTTPStatus

BASE_URL = 'https://ppe.hml.sebrae.al'

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
    
    def _get_headers(self):
        return {
            'X-Api-Key': self.api_key,
        }

    def get_certificates_to_download(
        self,
    ) -> PPEGetCertificatesToDownloadResponse:
        url = f"{self.base_url}/api/company/certificate/"
        
        response = self.http.get(url, headers=self._get_headers())

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

    def post_certificate(self, certificate: PPEPostCertificateRequest):
        url = f"{self.base_url}/api/company/certificate/"
        headers = self._get_headers()
        headers.update({'Content-Type': 'application/json'})
        
        response = self.http.post(url, headers=headers, json=certificate.model_dump(mode="json"))

        if response.status_code == HTTPStatus.CREATED:
            return response.json()
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(
                route=url,
                message=f"Bad request. The API Response down: {response.json()}",
            )
        elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise InternalServerError(
                route=url,
                message=f"Internal server error. The API Response down: {response.json()}",
                status_code=response.status_code
            )
        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error. The API Response down: {response.json()}",
                status_code=response.status_code
            )

        
    