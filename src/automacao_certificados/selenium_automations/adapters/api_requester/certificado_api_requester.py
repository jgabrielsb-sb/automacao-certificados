from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester

from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document
)

import requests

from http import HTTPStatus

from .exceptions import *

class CertificadoAPIRequester(BaseAPIRequester):
    """
    API requester for the Certificado.
    """
    def __init__(self, base_url: str):
        if not isinstance(base_url, str):
            raise ValueError("base_url must be a string")

        self.base_url = base_url
    
    def register_supplier(
        self, 
        supplier: dto_supplier.SupplierCreate
    ) -> dto_supplier.SupplierResponse:
        route = f"{self.base_url}/suppliers/"

        response = requests.post(
            url=route,
            json=supplier.model_dump(),
        )

        if response.status_code == HTTPStatus.CREATED:
            return dto_supplier.SupplierResponse(
                id=response.json()["id"],
                cnpj=response.json()["cnpj"],
            )
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(
                route=route,
                message=response.json()["message"],
            )
        elif response.status_code == HTTPStatus.CONFLICT:
            raise ConflictError(
                route=route,
                object="supplier",
                resource_name="cnpj",
                resource_value=supplier.cnpj,
            )
        else:
            raise UnexpectedError(
                route=route,
                message=response.json()["message"],
                status_code=response.status_code,
            )

    def get_supplier(
        self,
        filter: dto_supplier.SupplierFilter
    ) -> list[dto_supplier.SupplierResponse]:
        route = f"{self.base_url}/suppliers/"

        response = requests.get(
            url=route,
            params=filter.model_dump(),
        )
        if response.status_code == HTTPStatus.OK:
            if not response.json():
                raise NotFoundError(
                    route=route,
                    message=f"No suppliers found with the given filter: {filter.model_dump()}",
                )

            return [dto_supplier.SupplierResponse(
                id=supplier["id"],
                cnpj=supplier["cnpj"],
            ) for supplier in response.json()]

        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(
                route=route,
                message=response.json()["message"],
            )
        else:
            raise UnexpectedError(
                route=route,
                message=response.json()["message"],
                status_code=response.status_code,
            )

    def register_document(
        self, 
        document=dto_document.DocumentCreate
    ):
        route = f"{self.base_url}/documents/"

        response = requests.post(
            url=route,
            json=document.model_dump(),
        )

        if response.status_code == HTTPStatus.CREATED:
            return dto_document.DocumentResponse(
                id=response.json()["id"],
                supplier_id=response.json()["supplier_id"],
                document_type_id=response.json()["document_type_id"],
                identifier=response.json()["identifier"],
                expiration_date=response.json()["expiration_date"],
            )
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(
                route=route,
                message=response.json()["message"],
            )
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise NotFoundError(
                route=route,
                message=response.json()["message"]
            )
        else:
            raise UnexpectedError(
                route=route,
                message=response.json()["message"],
                status_code=response.status_code,
            )

    def get_document(
        self,
        filter: dto_document.DocumentFilter
    ) -> list[dto_document.DocumentResponse]:
        route = f"{self.base_url}/documents/"

        response = requests.get(
            url=route,
            params=filter.model_dump(),
        )
        if response.status_code == HTTPStatus.OK:
            if not response.json():
                raise NotFoundError(
                    route=route,
                    message=f"No documents found with the given filter: {filter.model_dump()}",
                )
            return [dto_document.DocumentResponse(
                id=document["id"],
                supplier_id=document["supplier_id"],
                document_type_id=document["document_type_id"],
                identifier=document["identifier"],
                expiration_date=document["expiration_date"],
            ) for document in response.json()]
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(
                route=route,
                message=response.json()["message"],
            )
        else:
            raise UnexpectedError(
                route=route,
                message=response.json()["message"],
                status_code=response.status_code,
            )
        
        
