from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.adapters import *

from unittest.mock import Mock

import pytest

from datetime import date

from automacao_certificados.selenium_automations.infra.api_requester import CertificadoAPIRequester

class TestGetOrCreateSupplier:
    def test_if_returns_existing_supplier_when_supplier_exists(
        self,
    ):
        api_mock = Mock(spec=CertificadoAPIRequester)
        api_mock.get_supplier.return_value = [
            dto_supplier.SupplierResponse(
                id=1,
                cnpj="12345678912"
            )
        ]

        api_persistence = CertificadoApiPersistance(api_requester=api_mock)
        supplier_response = api_persistence.get_or_create_supplier(
            dto_supplier.SupplierCreate(
                cnpj="12345678912"
            )
        )

        assert supplier_response.id == 1
        assert supplier_response.cnpj == "12345678912"

    def test_if_returns_created_supplier_when_supplier_does_not_exist(
        self,
    ):
        api_mock = Mock(spec=CertificadoAPIRequester)
        api_mock.get_supplier.side_effect = NotFoundError(
            route="test route",
            message="test message"
        )
        api_mock.register_supplier.return_value = dto_supplier.SupplierResponse(
            id=1,
            cnpj="12345678912"
        )

        api_persistence = CertificadoApiPersistance(api_requester=api_mock)
        supplier_response = api_persistence.get_or_create_supplier(
            dto_supplier.SupplierCreate(
                cnpj="12345678912"
            )
        )

        api_mock.get_supplier.assert_called_once_with(
            dto_supplier.SupplierFilter(cnpj="12345678912")
        )
        api_mock.register_supplier.assert_called_once_with(
            dto_supplier.SupplierCreate(cnpj="12345678912")
        )

        assert supplier_response.id == 1
        assert supplier_response.cnpj == "12345678912"

class TestSave:
    def test_sucess_case_with_already_created_supplier(
        self,
        monkeypatch
    ):
        document_persist = DocumentPersistanceInput(
            document_extracted=dto_document.DocumentExtracted(
                supplier=dto_supplier.Supplier(
                    cnpj="12345678912"
                ),
                document_type="CERTIFICADO TEST",
                identifier="test",
                expiration_date=date(2025, 1, 1)
            ),
            base64_pdf="PDF",
        )

        def fake_api_get_document_type(filter):
            return [
                dto_document_type.DocumentTypeResponse(
                    id=1,
                    name="CERTIFICADO TEST"
                )
            ]

        def fake_api_register_document(document):
            return dto_document.DocumentResponse(
                id=1,
                supplier_id=1,
                document_type_id=1,
                identifier="test",
                expiration_date=date(2025, 1, 1),
                base64_pdf="PDF",
            )

        api_mock = Mock(spec=CertificadoAPIRequester)
        monkeypatch.setattr(api_mock, "get_document_type", fake_api_get_document_type)
        monkeypatch.setattr(api_mock, "register_document", fake_api_register_document)

        api_persistence = CertificadoApiPersistance(api_requester=api_mock)

        def fakeget_or_create_supplier(supplier):
            return dto_supplier.SupplierResponse(
                id=1,
                cnpj="12345678912"
            )
        
        monkeypatch.setattr(api_persistence, "get_or_create_supplier", fakeget_or_create_supplier)
        api_persistence_result = api_persistence.save(input=document_persist)

        assert isinstance(api_persistence_result, DocumentPersistanceOutput)
        assert api_persistence_result.result == dto_document.DocumentResponse(
                id=1,
                supplier_id=1,
                document_type_id=1,
                identifier="test",
                expiration_date=date(2025, 1, 1),
                base64_pdf="PDF",
            ).model_dump(mode="json")

    def test_if_raises_document_type_not_found_error_if_document_type_does_not_exist(
        self,
        monkeypatch
    ):
        document_persist = DocumentPersistanceInput(
            document_extracted=dto_document.DocumentExtracted(
                supplier=dto_supplier.Supplier(
                    cnpj="12345678912"
                ),
                document_type="CERTIFICADO TEST",
                identifier="test",
                expiration_date=date(2025, 1, 1)
            ),
            base64_pdf="PDF",
        )

        def fake_api_get_document_type(filter):
            raise NotFoundError(
                route="test",
                message="test"
            )

        

        api_mock = Mock(spec=CertificadoAPIRequester)
        monkeypatch.setattr(api_mock, "get_document_type", fake_api_get_document_type)

        api_persistence = CertificadoApiPersistance(api_requester=api_mock)

        def fakeget_or_create_supplier(supplier):
            return dto_supplier.SupplierResponse(
                id=1,
                cnpj="12345678912"
            )
        monkeypatch.setattr(api_persistence, "get_or_create_supplier", fakeget_or_create_supplier)
        
        with pytest.raises(DocumentTypeNotFoundError) as e:
            api_persistence.save(document_persist)

        assert "Document Type not found" in str(e.value)

        


        



