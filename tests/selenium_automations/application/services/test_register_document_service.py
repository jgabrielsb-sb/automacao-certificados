import pytest
from unittest.mock import Base, Mock
from datetime import date

from automacao_certificados.selenium_automations.core.interfaces import BaseAPIRequester
from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier,
    dto_document_type,
)
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import NotFoundError
from automacao_certificados.selenium_automations.core.services.document.register_document_service import (
    RegisterDocumentService
)
from automacao_certificados.selenium_automations.core.services.document.exceptions import (
    DocumentTypeNotFoundError
)


class TestGetOrCreateSupplier:
    """
    Test class for the RegisterDocumentService._get_or_create_supplier() method.
    """
    def test_if_returns_existing_supplier_when_supplier_exists(
        self,
    ):
        api_mock = Mock(spec=BaseAPIRequester)
        api_mock.get_supplier.return_value = [
            dto_supplier.SupplierResponse(
                id=1,
                cnpj="12345678912"
            )
        ]

        service = RegisterDocumentService(api_requester=api_mock)
        supplier_response = service._get_or_create_supplier(
            dto_supplier.SupplierCreate(
                cnpj="12345678912"
            )
        )

        api_mock.get_supplier.assert_called_once_with(
            dto_supplier.SupplierFilter(cnpj="12345678912")
        )
        api_mock.register_supplier.assert_not_called()

        assert supplier_response.cnpj == "12345678912"
        assert supplier_response.id == 1

    def test_if_returns_created_supplier_when_supplier_does_not_exist(
        self
    ):
        cnpj, id = "12345678912", 1
        supplier_create = dto_supplier.SupplierCreate(cnpj=cnpj)
        supplier_response = dto_supplier.SupplierResponse(id=id, cnpj=cnpj)
        
        api_mock = Mock(spec=BaseAPIRequester)
        api_mock.get_supplier.side_effect = NotFoundError(
            route="test route",
            message="test message"
        )

        api_mock.register_supplier.return_value = supplier_response

        service = RegisterDocumentService(api_mock)
        supplier_response = service._get_or_create_supplier(
            supplier_create
        )

        assert supplier_response.cnpj == cnpj
        assert supplier_response.id == id

        api_mock.get_supplier.assert_called_once_with(
            dto_supplier.SupplierFilter(cnpj=cnpj)
        )
        api_mock.register_supplier.assert_called_once_with(
            supplier_create
        )

class TestRun:
    @pytest.fixture
    def base64_string(self):
        return "base 64 string"

    @pytest.fixture
    def document_extracted(self):
        return dto_document.DocumentExtracted(
            supplier=dto_supplier.Supplier(
                cnpj="12345678912"
            ),
            document_type="TEST DOCUMENT",
            identifier="123",
            expiration_date=date(2025,1,1)
        )

    def test_if_raises_document_type_not_found_error_if_document_type_does_not_exist(
        self,
        monkeypatch,
        base64_string,
        document_extracted
    ):
        cnpj, id = "12345678912", 1
        api_mock = Mock(spec=BaseAPIRequester)
        api_mock.get_document_type.side_effect = NotFoundError(
            route="test route",
            message="test message"
        )

        def fake_get_or_create_supplier(supplier):
            return dto_supplier.SupplierResponse(
                id=1,
                cnpj=cnpj
            )
        
        service = RegisterDocumentService(api_mock)
        monkeypatch.setattr(service, "_get_or_create_supplier", fake_get_or_create_supplier)

        with pytest.raises(DocumentTypeNotFoundError) as e:
            service.run(
                base64_string,
                document_extracted
            )

        assert "TEST DOCUMENT" in e.value.message

    def test_run_sucess(
        self,
        monkeypatch,
        base64_string,
        document_extracted
    ):
        cnpj, id = "12345678912", 1
        api_mock = Mock(spec=BaseAPIRequester)
        api_mock.get_document_type.return_value = dto_document_type.DocumentTypeResponse(
            id=1,
            name="TEST DOCUMENT"
        )
        api_mock.register_document.return_value = dto_document.DocumentResponse(
            id=1,
            supplier_id=1,
            document_type_id=1,
            identifier="123",
            expiration_date=date(2025, 1, 1),
        )

        def fake_get_or_create_supplier(supplier):
            return dto_supplier.SupplierResponse(
                id=1,
                cnpj=cnpj
            )   
     
        service = RegisterDocumentService(api_mock)
        monkeypatch.setattr(service, "_get_or_create_supplier", fake_get_or_create_supplier)

        document_created = service.run(
            base64_string,
            document_extracted
        )

        assert document_created.id == 1
        assert document_created.document_type_id == 1
        

       








        




























#         """
#         Test if the method returns existing supplier when supplier is found.
#         """
#         mock_api_requester = Mock(spec=BaseAPIRequester)
#         mock_supplier_response = dto_supplier.SupplierResponse(
#             id=1,
#             cnpj="12345678901234"
#         )
#         mock_api_requester.get_supplier.return_value = [mock_supplier_response]

#         service = RegisterDocumentService(api_requester=mock_api_requester)
#         supplier_create = dto_supplier.SupplierCreate(cnpj="12345678901234")
        
#         result = service._get_or_create_supplier(supplier_create)

#         assert result == mock_supplier_response
#         assert result.id == 1
#         assert result.cnpj == "12345678901234"
#         mock_api_requester.get_supplier.assert_called_once_with(
#             dto_supplier.SupplierFilter(cnpj="12345678901234")
#         )
#         mock_api_requester.register_supplier.assert_not_called()

#     def test_if_creates_supplier_when_supplier_not_found(self):
#         """
#         Test if the method creates supplier when supplier is not found.
#         """
#         mock_api_requester = Mock(spec=BaseAPIRequester)
#         mock_api_requester.get_supplier.side_effect = NotFoundError(
#             route="/suppliers",
#             message="Supplier not found"
#         )
        
#         mock_supplier_response = dto_supplier.SupplierResponse(
#             id=2,
#             cnpj="98765432109876"
#         )
#         mock_api_requester.register_supplier.return_value = mock_supplier_response

#         service = RegisterDocumentService(api_requester=mock_api_requester)
#         supplier_create = dto_supplier.SupplierCreate(cnpj="98765432109876")
        
#         result = service._get_or_create_supplier(supplier_create)

#         assert result == mock_supplier_response
#         assert result.id == 2
#         assert result.cnpj == "98765432109876"
#         mock_api_requester.get_supplier.assert_called_once_with(
#             dto_supplier.SupplierFilter(cnpj="98765432109876")
#         )
#         mock_api_requester.register_supplier.assert_called_once_with(
#             dto_supplier.SupplierCreate(cnpj="98765432109876")
#         )


# class TestRun:
#     """
#     Test class for the RegisterDocumentService.run() method.
#     """
#     def test_if_creates_supplier_and_registers_document_when_supplier_does_not_exist(self, monkeypatch):
#         """
#         Test if the method creates supplier and registers document when supplier doesn't exist.
#         """
#         mock_api_requester = Mock(spec=BaseAPIRequester)
        
#         # Mock supplier not existing
#         mock_api_requester.get_supplier.side_effect = NotFoundError(
#             route="/suppliers",
#             message="Supplier not found"
#         )
        
#         # Mock supplier registration
#         mock_supplier_response = dto_supplier.SupplierResponse(
#             id=1,
#             cnpj="12345678901234"
#         )
#         mock_api_requester.register_supplier.return_value = mock_supplier_response
        
#         # Mock document type retrieval
#         mock_document_type_response = [
#             dto_document_type.DocumentTypeResponse(
#                 id=1,
#                 name="CERTIFICADO CAIXA"
#             )
#         ]
#         mock_api_requester.get_document_type.return_value = mock_document_type_response
        
#         service = RegisterDocumentService(api_requester=mock_api_requester)
        
#         # Note: The implementation calls get_document_type with a string (document_extracted.document_type)
#         # but the interface expects DocumentTypeFilter. The implementation also expects get_document_type
#         # to return a single item with .id, but the interface returns a list.
#         # We'll mock get_document_type to return a single item to match what the implementation expects.
#         mock_document_type_single = dto_document_type.DocumentTypeResponse(
#             id=1,
#             name="CERTIFICADO CAIXA"
#         )
#         # Mock to accept string argument (as implementation does) and return single item
#         def mock_get_document_type(document_type_name):
#             return mock_document_type_single
        
#         mock_api_requester.get_document_type = mock_get_document_type
        
#         document_extracted = dto_document.DocumentExtracted(
#             supplier=dto_supplier.Supplier(cnpj="12345678901234"),
#             document_type="CERTIFICADO CAIXA",
#             identifier="2025110205156413642881",
#             expiration_date=date(2025, 12, 1)
#         )
        
#         base64_pdf = "base64_encoded_pdf_content"
        
#         # Note: The implementation has issues:
#         # 1. _get_or_create_supplier expects SupplierCreate but receives Supplier (type mismatch)
#         # 2. get_document_type is called with string instead of DocumentTypeFilter
#         # 3. Returns DocumentCreate instead of DocumentResponse
#         # The tests work around these issues by mocking appropriately
        
#         result = service.run(
#             base64_encoded_pdf=base64_pdf,
#             document_extracted=document_extracted
#         )
        
#         # Verify supplier was not found, then registered
#         # Note: _get_or_create_supplier receives Supplier but accesses .cnpj which works
#         mock_api_requester.get_supplier.assert_called()
#         mock_api_requester.register_supplier.assert_called_once_with(
#             dto_supplier.SupplierCreate(cnpj="12345678901234")
#         )
        
#         # Verify document type was retrieved (called with string as implementation does)
#         mock_api_requester.get_document_type.assert_called_once_with("CERTIFICADO CAIXA")
        
#         # Note: Current implementation returns DocumentCreate, not DocumentResponse
#         assert isinstance(result, dto_document.DocumentCreate)
#         assert result.supplier_id == 1
#         assert result.document_type_id == 1
#         assert result.identifier == "2025110205156413642881"
#         assert result.expiration_date == date(2025, 12, 1)

#     def test_if_gets_existing_supplier_and_registers_document_when_supplier_exists(self, monkeypatch):
#         """
#         Test if the method gets existing supplier and registers document when supplier exists.
#         """
#         mock_api_requester = Mock(spec=BaseAPIRequester)
        
#         # Mock supplier exists
#         mock_supplier_response = [
#             dto_supplier.SupplierResponse(
#                 id=2,
#                 cnpj="98765432109876"
#             )
#         ]
#         mock_api_requester.get_supplier.return_value = mock_supplier_response
        
#         # Mock document type retrieval
#         mock_document_type_response = [
#             dto_document_type.DocumentTypeResponse(
#                 id=1,
#                 name="CERTIFICADO CAIXA"
#             )
#         ]
#         mock_api_requester.get_document_type.return_value = mock_document_type_response
        
#         service = RegisterDocumentService(api_requester=mock_api_requester)
        
#         # Mock get_document_type to return a single item (as implementation expects)
#         mock_document_type_single = dto_document_type.DocumentTypeResponse(
#             id=1,
#             name="CERTIFICADO CAIXA"
#         )
#         def mock_get_document_type(document_type_name):
#             return mock_document_type_single
        
#         mock_api_requester.get_document_type = mock_get_document_type
        
#         document_extracted = dto_document.DocumentExtracted(
#             supplier=dto_supplier.Supplier(cnpj="98765432109876"),
#             document_type="CERTIFICADO CAIXA",
#             identifier="2025110205156413642882",
#             expiration_date=date(2025, 12, 2)
#         )
        
#         base64_pdf = "base64_encoded_pdf_content"
        
#         result = service.run(
#             base64_encoded_pdf=base64_pdf,
#             document_extracted=document_extracted
#         )
        
#         # Verify supplier was retrieved (not registered)
#         mock_api_requester.get_supplier.assert_called()
#         mock_api_requester.register_supplier.assert_not_called()
        
#         # Verify document type was retrieved (called with string as implementation does)
#         mock_api_requester.get_document_type.assert_called_once_with("CERTIFICADO CAIXA")
        
#         # Note: Current implementation returns DocumentCreate, not DocumentResponse
#         assert isinstance(result, dto_document.DocumentCreate)
#         assert result.supplier_id == 2
#         assert result.document_type_id == 1
#         assert result.identifier == "2025110205156413642882"
#         assert result.expiration_date == date(2025, 12, 2)

#     def test_if_raises_document_type_not_found_error_when_document_type_not_found(self, monkeypatch):
#         """
#         Test if the method raises DocumentTypeNotFoundError when document type is not found.
#         """
#         mock_api_requester = Mock(spec=BaseAPIRequester)
        
#         # Mock supplier exists
#         mock_supplier_response = [
#             dto_supplier.SupplierResponse(
#                 id=1,
#                 cnpj="12345678901234"
#             )
#         ]
#         mock_api_requester.get_supplier.return_value = mock_supplier_response
        
#         # Mock document type not found
#         mock_api_requester.get_document_type.side_effect = NotFoundError(
#             route="/document-types",
#             message="Document type not found"
#         )
        
#         service = RegisterDocumentService(api_requester=mock_api_requester)
        
#         # Mock document type not found
#         mock_api_requester.get_document_type.side_effect = NotFoundError(
#             route="/document-types",
#             message="Document type not found"
#         )
        
#         document_extracted = dto_document.DocumentExtracted(
#             supplier=dto_supplier.Supplier(cnpj="12345678901234"),
#             document_type="INVALID DOCUMENT TYPE",
#             identifier="2025110205156413642881",
#             expiration_date=date(2025, 12, 1)
#         )
        
#         base64_pdf = "base64_encoded_pdf_content"
        
#         with pytest.raises(DocumentTypeNotFoundError) as e:
#             service.run(
#                 base64_encoded_pdf=base64_pdf,
#                 document_extracted=document_extracted
#             )
        
#         assert "INVALID DOCUMENT TYPE" in e.value.message
#         assert "You must register it first" in e.value.message
        
#         # Verify supplier was retrieved/created
#         mock_api_requester.get_supplier.assert_called()
