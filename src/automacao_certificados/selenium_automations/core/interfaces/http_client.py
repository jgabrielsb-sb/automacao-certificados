from typing import (
    Any,
    Mapping,
    Optional,
    Protocol
)

class HttpResponse(Protocol):
    status_code: int
    def json(self) -> Any: ...
    

class HttpClient(Protocol):
    """
    Interface responsible for defining the contract for HTTP clients.
    """
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
        
        :param url: the URL to send the request to.
        :type url: str
        :param params: the query parameters to send with the request.
        :type params: dict
        :param headers: the headers to send with the request.
        :type headers: dict
        :param timeout: the timeout for the request.
        :type timeout: float
        :returns: the response from the request.
        :rtype: HttpResponse
        """
        pass

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
        
        :param url: the URL to send the request to.
        :type url: str
        :param params: the query parameters to send with the request.
        :type params: dict
        :param headers: the headers to send with the request.
        :type headers: dict

        :param timeout: the timeout for the request.
        :type timeout: float
        :param json: the JSON data to send with the request.
        :type json: dict
        :param data: the data to send with the request.
        :type data: dict
        :returns: the response from the request.
        :rtype: HttpResponse
        """
        pass


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
        :return: The response from the request.
        :rtype: HttpResponse
        """
        pass
        