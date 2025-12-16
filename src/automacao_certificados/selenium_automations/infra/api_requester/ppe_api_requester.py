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
        """
        The ppe api requester is responsible for making requests to the PPE API.
        """

        self.api_key = api_key
        self.base_url = base_url
        self.http = http
    
    def _get_headers(self) -> dict:
        """
        Gets the headers for the PPE API requests.

        :return: The headers.
        :rtype: dict
        """
        return {
            'X-Api-Key': self.api_key,
        }

    def _convert_response_to_certificates_to_download(
        self, 
        response_data: list[dict]
    ) -> list[CertificateToDownload]:
        """
        Converts the response data to a list of CertificateToDownload objects.

        :param response_data: The response data.
        :type response_data: list[dict]
        :return: The list of CertificateToDownload objects.
        :rtype: list[CertificateToDownload]
        """
        certificates_to_download = []
        
        for item in response_data:
            for certificate in item['certificates']:
                certificate_to_download = CertificateToDownload(
                    cnpj=item['cnpj'],
                    document_type=DocumentTypeEnum(certificate),
                )
                certificates_to_download.append(certificate_to_download)
        
        return certificates_to_download

    def get_certificates_to_download(
        self,
    ) -> list[CertificateToDownload]:
        """
        Gets the certificates to download from the PPE API.

        :return: The list of CertificateToDownload objects.
        :rtype: list[CertificateToDownload]
        :raises UnexpectedError: If an unexpected error occurs.
        """
        url = f"{self.base_url}/api/company/certificate/"
        
        response = self.http.get(url, headers=self._get_headers())

        if response.status_code == HTTPStatus.OK:
            return self._convert_response_to_certificates_to_download(response.json())
        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error. The API Response down: {response.content}",
                status_code=response.status_code
            )

    def post_certificate(
        self, 
        certificate: PPEPostCertificateRequest
    ) -> dict:
        """
        Posts a certificate to the PPE API.

        :param certificate: The certificate to post.
        :type certificate: PPEPostCertificateRequest
        :return: The response data.
        :rtype: dict
        :raises BadRequestError: If the request is bad.
        :raises InternalServerError: If the server is not responding.
        :raises UnexpectedError: If an unexpected error occurs.
        """
        url = f"{self.base_url}/api/company/certificate/"
        headers = self._get_headers()
        headers.update({'Content-Type': 'application/json'})
        
        response = self.http.post(url, headers=headers, json=certificate.model_dump(mode="json"))

        if response.status_code == HTTPStatus.OK:
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

    def block_certificate(self, cnpj: str, document_type: DocumentTypeEnum) -> dict:
        """
        Blocks a certificate from the PPE API.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :param document_type: The document type.
        :type document_type: DocumentTypeEnum
        :return: The response data.
        :rtype: dict
        """
        url = f"{self.base_url}/api/company/certificate/{cnpj}/pending/"
        json = {'certificate': document_type.value}
        
        response = self.http.patch(url, json=json, headers=self._get_headers())

        if response.status_code == HTTPStatus.OK:
            return response.json()
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

        