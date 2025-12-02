


import base64
from http import HTTPStatus
from automacao_certificados.selenium_automations.core.exceptions.adapters.api_requester_exceptions import CouldNotGeneratePDF, UnexpectedError
from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from automacao_certificados.selenium_automations.utils.utils import validate_cnpj

DEFAULT_BASE_URL = 'https://apiv3.directd.com.br'


class DirectDataAPIRequester:
    def __init__(
        self,
        http: HttpClient,
        token: str,
        base_url: str = DEFAULT_BASE_URL
    ):
        self.base_url = base_url
        self.http = http
        self.token = token

    def get_certificado_url(
        self,
        cnpj: str
    ) -> str:
        cnpj = validate_cnpj(cnpj)

        url = f"{self.base_url}/api/CertidaoConjuntaDebitosPessoaJuridica"

        response = self.http.get(url,params={
            "TOKEN": self.token,
            "CNPJ": cnpj,
            "GERARCOMPROVANTE": "Habilitar"
        })

        if response.status_code == HTTPStatus.OK:
            message = response.json()["metaDados"]["mensagem"]
            if not message == 'Sucesso':
                raise CouldNotGeneratePDF(
                    message=f"The api call on {url} could not generate PDF. The response message: {message}"
                )
            
            url = response.json()["metaDados"]["urlComprovante"]
            return url

        else:
            raise UnexpectedError(
                route=url,
                message=f"Unexpected Error on route {url}.Status code: {response.status_code}. API Response: {response.json()}",
                status_code=response.status_code
            )
    
    def get_certificado_base64(
        self,
        cnpj: str
    ) -> str:
        url = self.get_certificado_url(cnpj)
        response = self.http.get(url)
        base64_pdf = base64.b64encode(response.content).decode("utf-8")
        return base64_pdf
        


