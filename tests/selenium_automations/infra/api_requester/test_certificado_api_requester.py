from http import HTTPStatus
import pytest

from datetime import date

import respx
from httpx import Response

from automacao_certificados.selenium_automations.infra.api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document,
    dto_document_type,
    dto_log
)
from automacao_certificados.selenium_automations.adapters.http import HttpxClient, httpx_client

BASE_URL = "https://api.certificado.com"

api_requester = CertificadoAPIRequester(
    base_url=BASE_URL,
    http=HttpxClient()
)

class TestGetSupplier:
    @respx.mock
    def test_if_raises_not_found_error_if_there_is_not_supplier(self):
        mock_response = Response(
            200,
            json={
                "data": [],
                "meta": {
                    "page": 1,
                    "per_page": 10,
                    "total_items": 0,
                    "total_pages": 1,
                    "has_next": False,
                    "has_previous": False
                }
            }
        )

        route = respx.get(f"{BASE_URL}/api/v1/suppliers/").mock(mock_response)
       
        # Create the HttpxClient inside the mocked context
        http_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=http_client)

        with pytest.raises(NotFoundError) as e:
            api_requester.get_supplier(
                dto_supplier.SupplierCreate(cnpj="12345678912")
            )

        assert "12345678912" in str(e)
        

class TestRegisterSupplier:
    @respx.mock
    def test_success_response(self):
        route = respx.post(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(201, json={"id": 1, "cnpj": "12345678912"})
        )

        # Create the HttpxClient inside the mocked context
        http_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=http_client)

        supplier_response = api_requester.register_supplier(
            dto_supplier.SupplierCreate(cnpj="12345678912")
        )

        assert route.called
        assert supplier_response.cnpj == "12345678912"

    @respx.mock
    def test_conflict_response(self):
        route = respx.post(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(
                409, 
                json={
                    "error": "Conflict",
                    "message": "Supplier with cnpj 12345678912 already exists",
                    "path": "/api/v1/suppliers/",
                    "status_code": 409,
                    "timestamp": "2025-10-28T16:02:00Z"
                }
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(ConflictError) as e:
            api_requester.register_supplier(
                dto_supplier.SupplierCreate(cnpj="12345678912")
            )

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/suppliers/"
        assert "Supplier with cnpj 12345678912 already exists" in e.value.message

    @respx.mock
    def test_bad_request_response(self):
        route = respx.post(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(
                400,
                json={"message": "test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(BadRequestError) as e:
            api_requester.register_supplier(
                dto_supplier.SupplierCreate(cnpj="12345678912")
            )

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/suppliers/"
        assert e.value.message == "test message"

    @respx.mock
    def test_get_supplier_with_filter_success_response_with_results(self):
        supplier_filter = dto_supplier.SupplierFilter(cnpj="12345678912")
        
        route = respx.get(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(
                200,
                json={
                    "data": [
                        {
                            "id": 1,
                            "cnpj": "12345678912"
                        }
                    ]
                }
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        supplier_response = api_requester.get_supplier(supplier_filter)

        assert route.called
        assert isinstance(supplier_response, list)
        assert len(supplier_response) == 1
        assert supplier_response[0].id == 1
        assert supplier_response[0].cnpj == "12345678912"

    @respx.mock
    def test_get_supplier_with_filter_success_response_with_no_results(self):
        supplier_filter = dto_supplier.SupplierFilter(cnpj="12345678912")
        
        route = respx.get(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(
                200,
                json={"data": []}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(NotFoundError) as e:
            api_requester.get_supplier(supplier_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/suppliers/"
        assert f"{supplier_filter.model_dump()}" in e.value.message

    @respx.mock
    def test_unexpected_request_response(self):
        route = respx.post(f"{BASE_URL}/api/v1/suppliers/").mock(
            return_value=Response(
                500,
                json={"message": "test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(UnexpectedError) as e:
            api_requester.register_supplier(
                dto_supplier.SupplierCreate(cnpj="12345678912")
            )

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/suppliers/"
        assert e.value.message == "test message"
        assert e.value.status_code == 500

        


class TestRegisterDocument:
    @respx.mock
    def test_success_response(self):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31),
            base64_pdf="%PDF"
        )

        route = respx.post(f"{BASE_URL}/api/v1/documents/").mock(
            return_value=Response(
                201,
                json={
                    "id": 1,
                    "supplier_id": document_create.supplier_id,
                    "document_type_id": document_create.document_type_id,
                    "identifier": document_create.identifier,
                    "expiration_date": document_create.expiration_date.isoformat(),
                    "base64_pdf": "%PDF"
                }
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        document_response = api_requester.register_document(document_create)

        assert route.called
        assert isinstance(document_response, dto_document.DocumentResponse)
        assert document_response.id == 1
        assert document_response.supplier_id == 1
        assert document_response.document_type_id == 1
        assert document_response.identifier == "12345678912"
        assert document_response.expiration_date == date(2025, 12, 31)
        assert document_response.base64_pdf == "%PDF"

    @respx.mock
    def test_not_found_response(self):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31),
            base64_pdf="%PDF"
        )

        route = respx.post(f"{BASE_URL}/api/v1/documents/").mock(
            return_value=Response(
                404,
                json={"message": "supplier with id 1 not found"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(NotFoundError) as e:
            api_requester.register_document(document_create)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents/"
        assert "supplier with id 1 not found" in e.value.message

    @respx.mock
    def test_bad_request_response(self):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31),
            base64_pdf=b"%PDF"
        )

        route = respx.post(f"{BASE_URL}/api/v1/documents/").mock(
            return_value=Response(
                400,
                json={"message": "bad request test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(BadRequestError) as e:
            api_requester.register_document(document_create)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents/"
        assert "bad request test message" in e.value.message

    @respx.mock
    def test_unexpected_request_response(self):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31),
            base64_pdf=b"%PDF"
        )

        route = respx.post(f"{BASE_URL}/api/v1/documents/").mock(
            return_value=Response(
                500,
                json={"message": "unexpected test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(UnexpectedError) as e:
            api_requester.register_document(document_create)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents/"
        assert "unexpected test message" in e.value.message
        assert e.value.status_code == 500

class TestGetDocument:
    @respx.mock
    def test_get_document_with_filter_success_response_with_results(self):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31),
        )

        route = respx.get(f"{BASE_URL}/api/v1/documents").mock(
            return_value=Response(
                200,
                json={
                    "data": [
                        {
                            "id": 1,
                            "supplier_id": 1,
                            "document_type_id": 1,
                            "identifier": "12345678912",
                            "expiration_date": "2025-12-31",
                            "base64_pdf": "%PDF"
                        }
                    ]
                }
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        document_response = api_requester.get_document(document_filter)

        assert route.called
        assert isinstance(document_response, list)
        assert len(document_response) == 1
        assert document_response[0].id == 1
        assert document_response[0].supplier_id == 1
        assert document_response[0].document_type_id == 1
        assert document_response[0].identifier == "12345678912"
        assert document_response[0].expiration_date == date(2025, 12, 31)

    @respx.mock
    def test_get_document_with_filter_success_response_with_no_results(self):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        route = respx.get(f"{BASE_URL}/api/v1/documents").mock(
            return_value=Response(
                200,
                json={"data": []}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(NotFoundError) as e:
            api_requester.get_document(document_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert f"{document_filter.model_dump()}" in e.value.message

    @respx.mock
    def test_get_document_with_filter_bad_request_response(self):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        route = respx.get(f"{BASE_URL}/api/v1/documents").mock(
            return_value=Response(
                400,
                json={"message": "bad request test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(BadRequestError) as e:
            api_requester.get_document(document_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert "bad request test message" in e.value.message

    @respx.mock
    def test_get_document_with_filter_unexpected_response(self):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        route = respx.get(f"{BASE_URL}/api/v1/documents").mock(
            return_value=Response(
                500,
                json={"message": "unexpected test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(UnexpectedError) as e:
            api_requester.get_document(document_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert "unexpected test message" in e.value.message
        assert e.value.status_code == 500

class TestGetDocumentType:
    @respx.mock
    def test_get_document_type_with_filter_success_response_with_results(self):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )

        route = respx.get(f"{BASE_URL}/api/v1/document-types").mock(
            return_value=Response(
                200,
                json={
                    "data": [
                        {
                            "id": 1,
                            "name": "CERTIFICADO CAIXA"
                        }
                    ]
                }
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        document_type_response = api_requester.get_document_type(document_type_filter)

        assert route.called
        assert isinstance(document_type_response, list)
        assert len(document_type_response) == 1
        assert document_type_response[0].id == 1
        assert document_type_response[0].name == "CERTIFICADO CAIXA"

    @respx.mock
    def test_get_document_type_with_filter_success_response_with_no_results(self):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )

        route = respx.get(f"{BASE_URL}/api/v1/document-types").mock(
            return_value=Response(
                200,
                json={"data": []}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(NotFoundError) as e:
            api_requester.get_document_type(document_type_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert f"{document_type_filter.model_dump()}" in e.value.message

    @respx.mock
    def test_get_document_type_with_filter_bad_request_response(self):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )

        route = respx.get(f"{BASE_URL}/api/v1/document-types").mock(
            return_value=Response(
                400,
                json={"message": "bad request test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(BadRequestError) as e:
            api_requester.get_document_type(document_type_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert "bad request test message" in e.value.message

    @respx.mock
    def test_get_document_type_with_filter_unexpected_response(self):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )

        route = respx.get(f"{BASE_URL}/api/v1/document-types").mock(
            return_value=Response(
                500,
                json={"message": "unexpected test message"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(base_url=BASE_URL, http=httpx_client)

        with pytest.raises(UnexpectedError) as e:
            api_requester.get_document_type(document_type_filter)

        assert route.called
        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert "unexpected test message" in e.value.message
        assert e.value.status_code == 500

class TestRegisterLog:
    @respx.mock
    def test_sucess_response(self):
        json = {
                "timestamp": "2025-12-04T14:32:09.540Z",
                "facility": "string",
                "event_name": "string",
                "level": "DEBUG",
                "message": "string",
                "status": "SUCCESS",
                "request_id": "string",
                "details": {
                    "additionalProp1": {}
                },
                "result": "string",
                "id": 0
            }
        response_model = dto_log.LogResponse(**json)
        create_model = dto_log.LogCreate(**json)

        route = respx.post(
            url=f"{BASE_URL}/api/v1/logs/",
        ).mock(
            return_value=Response(
                status_code=HTTPStatus.CREATED, 
                json=response_model.model_dump(mode='json')
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(
            base_url=BASE_URL,
            http=httpx_client
        )

        response = api_requester.register_log(create_model)
        assert isinstance(response, dto_log.LogCreate)
    
    @respx.mock
    def test_another_response(self):
        json = {
                "timestamp": "2025-12-04T14:32:09.540Z",
                "facility": "string",
                "event_name": "string",
                "level": "DEBUG",
                "message": "string",
                "status": "SUCCESS",
                "request_id": "string",
                "details": {
                    "additionalProp1": {}
                },
                "result": "string",
                "id": 0
            }
        
        create_model = dto_log.LogCreate(**json)

        route = respx.post(
            url=f"{BASE_URL}/api/v1/logs/",
        ).mock(
            return_value=Response(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                json={"message": "internal server error"}
            )
        )

        httpx_client = HttpxClient()
        api_requester = CertificadoAPIRequester(
            base_url=BASE_URL,
            http=httpx_client
        )


        with pytest.raises(APIRequesterException) as e:
            response = api_requester.register_log(create_model)









    

        