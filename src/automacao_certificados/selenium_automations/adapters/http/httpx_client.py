import httpx

from typing import Any, Mapping, Optional

from automacao_certificados.selenium_automations.core.interfaces.http_client import (
    HttpClient, 
    HttpResponse
)

from automacao_certificados.selenium_automations.core.exceptions import (
    HttpClientException, 
    HttpClientSSLException
)

class HttpxClient(HttpClient):
    def __init__(self, base_timeout: float = 10.0):
        """
        The httpx client is an implementation of the http client port 
        that uses the httpx library to make http requests.
        """
        if not isinstance(base_timeout, float):
            raise ValueError("base_timeout must be a float")

        if base_timeout <= 0:
            raise ValueError("base_timeout must be greater than 0")

        self._client = httpx.Client(timeout=base_timeout)

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
        try:
            return self._client.get(
                url=url,
                params=params,
                headers=headers,
                timeout=timeout
            )
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                raise HttpClientSSLException(
                    f"SSL verification failed when calling {url}. Original exception:{str(e)}"
                ) from e
            
            raise HttpClientException(
                f"Error when calling {url}. Original exception: {str(e)}"
            )
        
    def post(
        self,
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None,
        json=None,
        data=None
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
        try:
            return self._client.post(
                url=url,
                params=params,
                headers=headers,
                timeout=timeout,
                json=json,
                data=data
            )
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                raise HttpClientSSLException(
                    f"SSL verification failed when calling {url}. Original exception:{str(e)}"
                ) from e
            
            raise HttpClientException(
                f"Error when calling {url}. Original exception: {str(e)}"
            )

    def patch(
        self,
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None,
        json=None
    ) -> HttpResponse:
        """
        Sends a PATCH request to the specified URL.
        """
        try:
            return self._client.patch(
                url=url,
                params=params,
                headers=headers,
                timeout=timeout,
                json=json
            )
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                raise HttpClientSSLException(
                    f"SSL verification failed when calling {url}. Original exception:{str(e)}"
                ) from e
            
            raise HttpClientException(
                f"Error when calling {url}. Original exception: {str(e)}"
            )