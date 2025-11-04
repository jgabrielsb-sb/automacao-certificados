import requests

from automacao_certificados.selenium_automations.core.interfaces.http_client import (
    HttpClient,
    HttpResponse
)

class RequestsClient(HttpClient):
    """
    Low-level adapter implementation of HttpClient 
    interface using requests library.
    """
    def __init__(self, base_timeout: float = 10.0):
        self._client = requests.Session()
        self._client.timeout = base_timeout

    def get(
        self,
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None
    ) -> HttpResponse:
        return self._client.get(
            url=url,
            params=params,
            headers=headers,
            timeout=timeout
        )

    def post(
        self,
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None,
        json=None
    ) -> HttpResponse:
        return self._client.post(
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            json=json
        )