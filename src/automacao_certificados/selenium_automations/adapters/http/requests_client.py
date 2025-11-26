import requests

from automacao_certificados.selenium_automations.core.interfaces.http_client import (
    HttpClient,
    HttpResponse
)

class RequestsClient(HttpClient):
    def __init__(self, base_timeout: float = 10.0):
        """
        The requests client is an implementation of the http client port 
        that uses the requests library to make http requests.
        """
        if not isinstance(base_timeout, float):
            raise ValueError("base_timeout must be a float")

        if base_timeout <= 0:
            raise ValueError("base_timeout must be greater than 0")

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
        """
        Sends a GET request to the specified URL.

        :param url: The URL to send the request to.
        :type url: str
        :param params: The query parameters to send with the request.
        :type params: dict
        :param headers: The headers to send with the request.
        :type headers: dict
        :param timeout: The timeout for the request.
        :type timeout: float
        :return: The response from the request.
        :rtype: HttpResponse
        """
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
        """
        Sends a POST request to the specified URL.

        :param url: The URL to send the request to.
        :type url: str
        :param params: The query parameters to send with the request.
        :type params: dict
        :param headers: The headers to send with the request.
        :type headers: dict
        :param timeout: The timeout for the request.
        :type timeout: float
        :param json: The JSON data to send with the request.
        :type json: dict
        :param data: The data to send with the request.
        :type data: dict
        :return: The response from the request.
        :rtype: HttpResponse
        """
        return self._client.post(
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            json=json
        )