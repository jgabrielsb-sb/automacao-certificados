import pytest
from unittest.mock import Mock
from datetime import date

from automacao_certificados.selenium_automations.core.interfaces import BaseAPIRequester
from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier,
    dto_document_type,
)
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import NotFoundError
from automacao_certificados.selenium_automations.application.services.api import CertificadoAPIService


class TestIsSupplierAlreadyRegistered:
    """
    Test class for the CertificadoAPIService.is_supplier_already_registered() method.
    """
    def test_if_returns_true_when_supplier_exists(self):
        """
        Test if the method returns True when supplier is found.
        """
        mock_api_requester = Mock(spec=BaseAPIRequester)
        mock_api_requester.get_supplier.return_value = [
            dto_supplier.SupplierResponse(id=1, cnpj="12345678901234")
        ]

        service = CertificadoAPIService(api_requester=mock_api_requester)
        result = service.is_supplier_already_registered(cnpj="12345678901234")

        assert result is True
        mock_api_requester.get_supplier.assert_called_once_with(
            filter=dto_supplier.SupplierFilter(cnpj="12345678901234")
        )

    def test_if_returns_false_when_supplier_not_found(self):
        """
        Test if the method returns False when supplier is not found (raises NotFoundError).
        """
        mock_api_requester = Mock(spec=BaseAPIRequester)
        mock_api_requester.get_supplier.side_effect = NotFoundError(
            route="/suppliers",
            message="Supplier not found"
        )

        service = CertificadoAPIService(api_requester=mock_api_requester)
        result = service.is_supplier_already_registered(cnpj="12345678901234")

        assert result is False
        mock_api_requester.get_supplier.assert_called_once_with(
            filter=dto_supplier.SupplierFilter(cnpj="12345678901234")
        )


class TestRegisterDocument:
    """
    Test class for the CertificadoAPIService.register_document() method.
    """
    def test_if_registers_supplier_when_supplier_does_not_exist(self):
        """
        Test if the method registers a new supplier when supplier doesn't exist.
        """
        mock_api_requester = Mock(spec=BaseAPIRequester)
        
        # Mock supplier not existing
        mock_api_requester.get_supplier.side_effect = NotFoundError(
            route="/suppliers",
            message="Supplier not found"
        )
        
        # Mock supplier registration
        mock_supplier_response = dto_supplier.SupplierResponse(
            id=1,
            cnpj="12345678901234"
        )
        mock_api_requester.register_supplier.return_value = mock_supplier_response
        
        # Mock document type retrieval
        mock_document_type_response = [
            dto_document_type.DocumentTypeResponse(
                id=1,
                name="CERTIFICADO CAIXA"
            )
        ]
        mock_api_requester.get_document_type.return_value = mock_document_type_response
        
        # Mock document registration
        mock_document_response = dto_document.DocumentResponse(
            id=1,
            supplier_id=1,
            document_type_id=1,
            identifier="2025110205156413642881",
            expiration_date=date(2025, 12, 1)
        )
        mock_api_requester.register_document.return_value = mock_document_response
        
        service = CertificadoAPIService(api_requester=mock_api_requester)
        
        document_extracted = dto_document.DocumentExtracted(
            supplier=dto_supplier.Supplier(cnpj="12345678901234"),
            document_type="CERTIFICADO CAIXA",
            identifier="2025110205156413642881",
            expiration_date=date(2025, 12, 1)
        )
        
        result = service.register_document(document=document_extracted)
        
        # Verify supplier was not found, then registered
        mock_api_requester.get_supplier.assert_called_once_with(
            filter=dto_supplier.SupplierFilter(cnpj="12345678901234")
        )
        mock_api_requester.register_supplier.assert_called_once_with(
            supplier=dto_supplier.SupplierCreate(cnpj="12345678901234")
        )
        
        # Verify document type was retrieved
        mock_api_requester.get_document_type.assert_called_once_with(
            filter=dto_document_type.DocumentTypeFilter(name="CERTIFICADO CAIXA")
        )
        
        # Verify document was registered
        mock_api_requester.register_document.assert_called_once_with(
            document=dto_document.DocumentCreate(
                supplier_id=1,
                document_type_id=1,
                identifier="2025110205156413642881",
                expiration_date=date(2025, 12, 1)
            )
        )
        
        # Verify result
        assert isinstance(result, dto_document.DocumentResponse)
        assert result.id == 1
        assert result.supplier_id == 1
        assert result.document_type_id == 1
        assert result.identifier == "2025110205156413642881"
        assert result.expiration_date == date(2025, 12, 1)

    def test_if_gets_existing_supplier_when_supplier_exists(self):
        """
        Test if the method gets existing supplier when supplier already exists.
        """
        mock_api_requester = Mock(spec=BaseAPIRequester)
        
        # Mock supplier exists
        mock_supplier_response = [
            dto_supplier.SupplierResponse(
                id=2,
                cnpj="98765432109876"
            )
        ]
        mock_api_requester.get_supplier.return_value = mock_supplier_response
        
        # Mock document type retrieval
        mock_document_type_response = [
            dto_document_type.DocumentTypeResponse(
                id=1,
                name="CERTIFICADO CAIXA"
            )
        ]
        mock_api_requester.get_document_type.return_value = mock_document_type_response
        
        # Mock document registration
        mock_document_response = dto_document.DocumentResponse(
            id=2,
            supplier_id=2,
            document_type_id=1,
            identifier="2025110205156413642882",
            expiration_date=date(2025, 12, 2)
        )
        mock_api_requester.register_document.return_value = mock_document_response
        
        service = CertificadoAPIService(api_requester=mock_api_requester)
        
        document_extracted = dto_document.DocumentExtracted(
            supplier=dto_supplier.Supplier(cnpj="98765432109876"),
            document_type="CERTIFICADO CAIXA",
            identifier="2025110205156413642882",
            expiration_date=date(2025, 12, 2)
        )
        
        result = service.register_document(document=document_extracted)
        
        # Verify supplier was retrieved (not registered)
        mock_api_requester.get_supplier.assert_called_with(
            filter=dto_supplier.SupplierFilter(cnpj="98765432109876")
        )
        mock_api_requester.register_supplier.assert_not_called()
        
        # Verify document type was retrieved
        mock_api_requester.get_document_type.assert_called_with(
            filter=dto_document_type.DocumentTypeFilter(name="CERTIFICADO CAIXA")
        )
        
        # Verify document was registered with correct supplier_id from existing supplier
        mock_api_requester.register_document.assert_called_with(
            document=dto_document.DocumentCreate(
                supplier_id=2,
                document_type_id=1,
                identifier="2025110205156413642882",
                expiration_date=date(2025, 12, 2)
            )
        )
        
        # Verify result
        assert isinstance(result, dto_document.DocumentResponse)
        assert result.id == 2
        assert result.supplier_id == 2
        assert result.document_type_id == 1
        assert result.identifier == "2025110205156413642882"
        assert result.expiration_date == date(2025, 12, 2)

