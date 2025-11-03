import pytest

from unittest.mock import Mock

import requests

from automacao_certificados.selenium_automations.adapters.api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import BadRequestError, ConflictError, UnexpectedError
from automacao_certificados.selenium_automations.core.models import dto_supplier

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



        

    
            


        



    
