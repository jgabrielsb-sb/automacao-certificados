from automacao_certificados.selenium_automations.core.interfaces import (
    BaseAPIRequester,
    HttpClient
)

from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document,
    dto_document_type
)


from http import HTTPStatus

from .exceptions import *
from .error_mapping import map_error_response

class CertificadoAPIRequester(BaseAPIRequester):
    """
    API requester for the Certificado.
    """
    def __init__(
        self, 
        base_url: str,
        http: HttpClient
    ):
        if not isinstance(base_url, str):
            raise ValueError("base_url must be a string")

        self.base_url = base_url
        self.http = http
    
    def register_supplier(
        self, 
        supplier: dto_supplier.SupplierCreate
    ) -> dto_supplier.SupplierResponse:
        """
        Register a new supplier.
        Arguments:
            supplier
        Returns:
            The created supplier
        Raises:
            ConflictError: if a supplier with the same cnoj already exists.
            UnexpectedError: if an uenxpected error occurs
        """
        
        route = f"{self.base_url}/api/v1/suppliers/"
        response = self.http.post(url=route, json=supplier.model_dump(mode="json"))

        if response.status_code == HTTPStatus.CREATED:
            return dto_supplier.SupplierResponse(
                id=response.json()["id"],
                cnpj=response.json()["cnpj"],
            )
        else:
            return map_error_response(
                route,
                response.status_code,
                response.json()
            )


    def get_supplier(
        self,
        filter: dto_supplier.SupplierFilter
    ) -> list[dto_supplier.SupplierResponse]:
        """
        Get a list of suppliers.
        Arguments:
            filter
        Returns:
            A list of suppliers
        Raises:
            NotFoundError: if no suppliers are found with the given filter.
            UnexpectedError: if an unexpected error occurs
        """
        route = f"{self.base_url}/api/v1/suppliers/"
        
        response = self.http.get(url=route, params=filter.model_dump(mode="json"))
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            data = response.json().get("data", [])
            if not data:
                raise NotFoundError(
                    route=route,
                    message=f"No suppliers found with the given filter: {filter.model_dump()}",
                )

            return [dto_supplier.SupplierResponse(**x) for x in data]
        else:
            map_error_response(route, status_code, response.json())

    def register_document(
        self, 
        document=dto_document.DocumentCreate
    ):
        """
        Register a new document.
        Arguments:
            document
        Returns:
            The created document
        Raises:
            UnexpectedError: if an unexpected error occurs
        """
        route = f"{self.base_url}/api/v1/documents/"

        response = self.http.post(route, json=document.model_dump(mode="json"))
        status_code = response.status_code


        if response.status_code == HTTPStatus.CREATED:
            return dto_document.DocumentResponse(**response.json())
        else:
            map_error_response(route, status_code, body=response.json())
        

    def get_document(
        self,
        filter: dto_document.DocumentFilter
    ) -> list[dto_document.DocumentResponse]:
        """
        Get a list of documents.
        Arguments:
            filter
        Returns:
            A list of documents
        Raises:
            NotFoundError: if no documents are found with the given filter.
            UnexpectedError: if an unexpected error occurs
        """
        route = f"{self.base_url}/api/v1/documents"

        response = self.http.get(url=route, params=filter.model_dump(mode="json"))
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            data = response.json().get("data", [])
            if not data:
                raise NotFoundError(
                    route=route,
                    message=f"No documents found with the given filter: {filter.model_dump()}"
                )
            return [dto_document.DocumentResponse(**x) for x in data]
        else:
            map_error_response(route, status_code, body=response.json())

    def get_document_type(
        self,
        filter: dto_document_type.DocumentTypeFilter
    ) -> list[dto_document_type.DocumentTypeResponse]:
        """
        Get a list of document types.
        Arguments:
            filter
        Returns:
            A list of document types
        Raises:
            NotFoundError: if no document types are found with the given filter.
            UnexpectedError: if an unexpected error occurs
        """
        route = f"{self.base_url}/api/v1/document-types"

        response = self.http.get(url=route, params=filter.model_dump(mode="json"))
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            data = response.json().get("data", [])
            if not data:
                raise NotFoundError(
                    route=route,
                    message=f"No document types found with the given filter: {filter.model_dump()}"
                )
            return [dto_document_type.DocumentTypeResponse(**x) for x in data]
        else:
            map_error_response(route, status_code, body=response.json())
        
        
