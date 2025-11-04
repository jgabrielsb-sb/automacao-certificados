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
    Base interface for HTTP Clients
    """
    def get(
        self, 
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None
    ) -> HttpResponse: ...

    def post(
        self,
        url: str,
        *,
        params=None,
        headers=None,
        timeout=None,
        json=None
    ) -> HttpResponse: ...


    