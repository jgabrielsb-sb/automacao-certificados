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
        if not isinstance(base_url, str):
            raise ValueError("base_url must be a string")

        self.base_url = base_url
        self.http = http

    def _get_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',}

        data_to_send = {
            'username': settings.nota_facil_username, 
            'password': settings.nota_facil_password,
            'grant_type': 'password',
            'scope': 'read:self'
        }

        response = self.http.post(url=f"https://api.notafacil.hml.sebrae.al/ppe/api/v1/token", data=data_to_send, headers=headers)
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            token = response.json().get('access_token')
            return token
        else:
            raise UnexpectedError(
                route=f"{self.base_url}/token",
                message=f"Unexpected error. The API Response down: {response.text}",
                status_code=status_code
            )

    def _get_headers(self) -> dict:
        token = self._get_token()
        headers = {
            'Authorization': f'Bearer {token}',
        }
        return headers

    def get_company(
        self,
        cnpj: str
    ) -> ReceitaAPIGetCompanyResponse:
        url = f"{self.base_url}/empresa-receita/get-by-cnpj/{cnpj}"
        response = self.http.get(url, headers=self._get_headers())
    
        if response.status_code == HTTPStatus.OK:
            data = response.json()["data"]
            return ReceitaAPIGetCompanyResponse.model_validate(data)
        
        elif response.status_code == HTTPStatus.NOT_FOUND:
            if response.json().get("detail") and "Not Found" in response.json().get("detail"):
                raise RouteNotFoundError(
                    route=url, 
                    message=f"Route not found: {url}",
                    status_code=response.status_code
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