import pytest

from unittest.mock import Mock

import requests

from datetime import date

from automacao_certificados.selenium_automations.adapters.api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import *
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document,
    dto_document_type
)

BASE_URL = "https://api.certificado.com"
api_requester = CertificadoAPIRequester(
    base_url=BASE_URL
)

class TestRegisterSupplier:
    def test_sucess_response(
        self,
        monkeypatch,
    ):
        supplier_create = dto_supplier.SupplierCreate(
            cnpj="12345678912"
        )

        def mock_fake_post(
            url,
            json,
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = {
                "id": 1,
                "cnpj": supplier_create.cnpj
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        supplier_response = api_requester.register_supplier(
            supplier_create
        )

        assert isinstance(supplier_response, dto_supplier.SupplierResponse)
        assert supplier_response.id == 1
        assert supplier_response.cnpj == "12345678912"

    def test_conflict_response(
        self,
        monkeypatch,
    ):
        supplier_create = dto_supplier.SupplierCreate(
            cnpj="12345678912"
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 409
            response.json.return_value = {
                "error": "Conflict",
                "message": "Supplier with cnpj 12345678912 already exists",
                "path": "/api/v1/suppliers/",
                "status_code": 409,
                "timestamp": "2025-10-28T16:02:00Z"
                }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(ConflictError) as e:
            api_requester.register_supplier(
                supplier_create
            )

        
        assert e.value.object == 'supplier'
        assert e.value.resource_name == "cnpj"
        assert e.value.resource_value == "12345678912"

    def test_bad_request_response(
        self,
        monkeypatch,
    ):
        supplier_create = dto_supplier.SupplierCreate(
            cnpj="12345678912"
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 400
            response.json.return_value = {
                "message": "test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(BadRequestError) as e:
            api_requester.register_supplier(
                supplier_create
            )

            assert e.value.route == f"{BASE_URL}/suppliers"
            assert e.value.message == "test message"

    def test_get_supplier_with_filter_sucess_response_with_results(
        self,
        monkeypatch,
    ):
        supplier_filter = dto_supplier.SupplierFilter(
            cnpj="12345678912"
        )
        
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                "data": [
                    {
                        "id": 1, 
                        "cnpj": "12345678912"
                    }
                ]
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )

        supplier_response = api_requester.get_supplier(
            supplier_filter
        )

        assert isinstance(supplier_response, list)
        assert len(supplier_response) == 1
        assert supplier_response[0].id == 1
        assert supplier_response[0].cnpj == "12345678912"

    def test_get_supplier_with_filter_sucess_response_with_no_results(
        self,
        monkeypatch,
    ):
        supplier_filter = dto_supplier.SupplierFilter(
            cnpj="12345678912"
        )
        
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                "data": []
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(NotFoundError) as e:
            api_requester.get_supplier(
                supplier_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/suppliers/"
        assert f"{supplier_filter.model_dump()}" in e.value.message

    def test_unexpected_request_response(
        self,
        monkeypatch,
    ):
        supplier_create = dto_supplier.SupplierCreate(
            cnpj="12345678912"
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 500
            response.json.return_value = {
                "message": "test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(UnexpectedError) as e:
            api_requester.register_supplier(
                supplier_create
            )

            assert e.value.route == f"{BASE_URL}/suppliers"
            assert e.value.message == "test message"

class TestRegisterDocument:
    def test_sucess_response(
        self,
        monkeypatch,
    ):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_post(
            url,
            json,
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = {
                "id": 1,
                "supplier_id": document_create.supplier_id,
                "document_type_id": document_create.document_type_id,
                "identifier": document_create.identifier,
                "expiration_date": document_create.expiration_date.isoformat()
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        document_response = api_requester.register_document(
            document_create
        )

        assert isinstance(document_response, dto_document.DocumentResponse)
        assert document_response.id == 1
        assert document_response.supplier_id == 1
        assert document_response.document_type_id == 1
        assert document_response.identifier == "12345678912"
        assert document_response.expiration_date == date(2025, 12, 31)

    def test_not_found_response(
        self,
        monkeypatch,
    ):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 404
            response.json.return_value = {
                "message": "supplier with id 1 not found"
                }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(NotFoundError) as e:
            api_requester.register_document(
                document_create
            )

        assert e.value.route == f"{BASE_URL}/api/v1/documents/"
        assert "supplier with id 1 not found" in e.value.message

    def test_bad_request_response(
        self,
        monkeypatch,
    ):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 400
            response.json.return_value = {
                "message": "bad request test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(BadRequestError) as e:
            api_requester.register_document(
                document_create
            )

        assert e.value.route == f"{BASE_URL}/api/v1/documents/"
        assert "bad request test message" in e.value.message

    def test_unexpected_request_response(
        self,
        monkeypatch,
    ):
        document_create = dto_document.DocumentCreate(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_post(
            url,
            json
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 500
            response.json.return_value = {
                "message": "unexpected test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "post",
            mock_fake_post
        )

        with pytest.raises(UnexpectedError) as e:
            api_requester.register_document(
                document_create
            )

            assert e.value.route == f"{BASE_URL}/api/v1/documents/"
            assert e.value.message == "test message"

class TestGetDocument:
    def test_get_document_with_filter_sucess_response_with_results(
        self,
        monkeypatch,
    ):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                    "data": [
                        {
                            "id": 1, 
                            "supplier_id": 1, 
                            "document_type_id": 1, 
                            "identifier": "12345678912", 
                            "expiration_date": "2025-12-31"
                        }
                    ]
                }
            

            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )

        document_response = api_requester.get_document(
            document_filter
        )

        assert isinstance(document_response, list)
        assert len(document_response) == 1
        assert document_response[0].id == 1
        assert document_response[0].supplier_id == 1
        assert document_response[0].document_type_id == 1
        assert document_response[0].identifier == "12345678912"
        assert document_response[0].expiration_date == date(2025, 12, 31)
    
    def test_get_document_with_filter_sucess_response_with_no_results(
        self,
        monkeypatch,
    ):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                "data": []
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(NotFoundError) as e:
            api_requester.get_document(
                document_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert f"{document_filter.model_dump()}" in e.value.message

    def test_get_document_with_filter_bad_request_response(
        self,
        monkeypatch,
    ):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 400
            response.json.return_value = {
                "message": "bad request test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(BadRequestError) as e:
            api_requester.get_document(
                document_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert "bad request test message" in e.value.message

    def test_get_document_with_filter_unexpected_response(
        self,
        monkeypatch,
    ):
        document_filter = dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id="1",
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )

        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 500
            response.json.return_value = {
                "message": "unexpected test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(UnexpectedError) as e:
            api_requester.get_document(
                document_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/documents"
        assert "unexpected test message" in e.value.message
        assert e.value.status_code == 500

class TestGetDocumentType:
    def test_get_document_type_with_filter_sucess_response_with_results(
        self,
        monkeypatch,
    ):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )

        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                "data": [
                    {
                        "id": 1,
                        "name": "CERTIFICADO CAIXA"
                    }
                ]
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )

        document_type_response = api_requester.get_document_type(
            document_type_filter
        )

        assert isinstance(document_type_response, list)
        assert len(document_type_response) == 1
        assert document_type_response[0].id == 1
        assert document_type_response[0].name == "CERTIFICADO CAIXA"

    def test_get_document_type_with_filter_sucess_response_with_no_results(
        self,
        monkeypatch,
    ):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = {
                "data": []
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(NotFoundError) as e:
            api_requester.get_document_type(
                document_type_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert f"{document_type_filter.model_dump()}" in e.value.message

    def test_get_document_type_with_filter_bad_request_response(
        
        self,
        monkeypatch,
    ):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )   
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 400
            response.json.return_value = {
                "message": "bad request test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(BadRequestError) as e:
            api_requester.get_document_type(
                document_type_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert "bad request test message" in e.value.message

    def test_get_document_type_with_filter_unexpected_response(
        self,
        monkeypatch,
    ):
        document_type_filter = dto_document_type.DocumentTypeFilter(
            name="CERTIFICADO CAIXA"
        )
        def mock_fake_get(
            url,
            params
        ):
            response = Mock(spec=requests.Response)
            response.status_code = 500
            response.json.return_value = {
                "message": "unexpected test message"
            }
            return response

        monkeypatch.setattr(
            requests,
            "get",
            mock_fake_get
        )
        with pytest.raises(UnexpectedError) as e:
            api_requester.get_document_type(
                document_type_filter
            )

        assert e.value.route == f"{BASE_URL}/api/v1/document-types"
        assert "unexpected test message" in e.value.message
        assert e.value.status_code == 500

        