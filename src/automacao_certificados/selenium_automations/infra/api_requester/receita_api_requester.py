from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.config import settings

from http import HTTPStatus
BASE_URL = "https://api.notafacil.hml.sebrae.al/receita/api/v1"


class ReceitaAPIRequester:
    def __init__(
        self,
        http: HttpClient,
        base_url: str = BASE_URL,
    ):
        """
        The receita api requester is responsible for making requests to the Receita API.
        """
        if not isinstance(base_url, str):
            raise ValueError("base_url must be a string")

        self.base_url = base_url
        self.http = http

    def get_company(
        self,
        cnpj: str
    ) -> ReceitaAPIGetCompanyResponse:
        """
        Gets the company by cnpj using the Receita API.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The company.
        :rtype: ReceitaAPIGetCompanyResponse
        :raises RouteNotFoundError: If the route is not found.
        :raises NotFoundError: If the company is not found.
        :raises UnexpectedError: If an unexpected error occurs.
        """
        url = f"{self.base_url}/receita/api/v1/empresa-receita/get-by-cnpj/{cnpj}"
        response = self.http.get(url)
    
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            return ReceitaAPIGetCompanyResponse.model_validate(data)
        
        elif response.status_code == HTTPStatus.NOT_FOUND:
            if response.json().get("detail") and "Not Found" in response.json().get("detail"):
                raise RouteNotFoundError(
                    route=url, 
                    message=f"Route not found: {url}",
                )
            
            raise NotFoundError(
                route=url, 
                message=f"Company not found: {cnpj}. API Response: {response.json()}",
                status_code=response.status_code
            )
        
        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected error: {response.json()}. API Response: {response.json()}", 
                status_code=response.status_code
            )