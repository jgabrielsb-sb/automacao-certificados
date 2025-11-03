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

    def register_document(
        self, document
    ):
        pass

        
        
