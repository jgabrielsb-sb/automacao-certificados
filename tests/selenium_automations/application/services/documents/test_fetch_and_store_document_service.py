from automacao_certificados.selenium_automations.application.services import (
    FetchAndStoreDocumentService,
    FetchAndStoreResult
)

from automacao_certificados.selenium_automations.core.interfaces import (
    DocumentAcquisitionPort, DocumentRequest, DocumentResult,
    DocumentPersistancePort, DocumentPersist, DocumentPersistResult
)

from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier
)

from datetime import date

import pytest

@pytest.fixture
def mock_document_acquisition_port():
    class MockDocumentAcquisitionImplementation(DocumentAcquisitionPort):
        def acquire(self, req: DocumentRequest) -> DocumentResult:
            return DocumentResult(
                document_extracted = dto_document.DocumentExtracted(
                    dto_supplier.Supplier(
                        cnpj="12345678912"
                    )
                ),
                base64_pdf="BASE64PDF"
            )

    return MockDocumentAcquisitionImplementation

@pytest.fixture
def mock_document_persistence_port():
    class MockDocumentPersistenceImplementation(DocumentPersistancePort):
        def save(self, document: DocumentPersist) -> DocumentPersistResult:
            return DocumentPersistResult(
                result={"message": "element saved"}
            )

    return MockDocumentPersistenceImplementation

class TestInit:
    def test_if_raises_value_error_if_acquisition_is_not_document_acquisition_port(
        self,
        mock_document_persistence_port
    ):
        with pytest.raises(ValueError) as e:
            FetchAndStoreDocumentService(
                acquisition="wrong type",
                persistence=mock_document_persistence_port
            )

        assert "acquisition" in str(e.value)

    def test_if_raises_value_error_if_persistence_is_not_document_persistence_port(
        self,
        mock_document_acquisition_port
    ):
        with pytest.raises(ValueError) as e:
            FetchAndStoreDocumentService(
                acquisition=mock_document_acquisition_port,
                persistence="wrong type"
            )

        assert "persistence" in str(e.value)

class TestExecute:
    def test_if_raises_value_error_if_document_result_is_not_document_result(
        self,
        mock_document_acquisition_port
    ):
        with pytest.raises(ValueError) as e:
            FetchAndStoreDocumentService(
                acquisition=mock_document_acquisition_port,
                persistence=mock_document_persistence_port
            ).execute("wrong type")

        assert "document_result must be a DocumentResult" in str(e.value)

    def test_if_raises_value_error_if_document_result_is_not_document_result(
        self,
        mock_document_acquisition_port,
        mock_document_persistence_port,
        monkeypatch
    ):

        def mock_fake_acquire(req: DocumentRequest) -> DocumentResult:
            return "wrong type"

        monkeypatch.setattr(mock_document_acquisition_port, "acquire", mock_fake_acquire)
        
        with pytest.raises(ValueError) as e:
            FetchAndStoreDocumentService(
                acquisition=mock_document_acquisition_port,
                persistence=mock_document_persistence_port
            ).execute(
                DocumentRequest(
                    cnpj="12345678912"
                )
            )

        assert "document_result must be a DocumentResult" in str(e.value)

    def test_sucess_case(
        self,
        mock_document_acquisition_port,
        mock_document_persistence_port,
        monkeypatch
    ):
        def mock_validate_document_file(base64_pdf: str) -> None:
            return None
        
        # patch in the module where it's *used*
        monkeypatch.setattr(
            "automacao_certificados.selenium_automations.application.services.documents.fetch_and_store_document_service.validate_document_file",
            mock_validate_document_file,
        )

        fetch_and_store_result = FetchAndStoreDocumentService(
            acquisition=mock_document_acquisition_port,
            persistence=mock_document_persistence_port
        )

        monkeypatch.setattr(fetch_and_store_result, "_acquisition", mock_document_acquisition_port)

        def mock_fake_acquire(req: DocumentRequest) -> DocumentResult:
            return DocumentResult(
                document_extracted=dto_document.DocumentExtracted(
                    supplier=dto_supplier.Supplier(
                        cnpj="12345678912"
                    ),
                    document_type="CERTIDAO",
                    identifier="12345678912",
                    expiration_date=date(2025, 1, 1)
                ),
                base64_pdf="BASE64PDF"
            )

        def mock_fake_save(document: DocumentPersist) -> DocumentPersistResult:
            return DocumentPersistResult(
                result={"message": "element saved"}
            )

        monkeypatch.setattr(mock_document_acquisition_port, "acquire", mock_fake_acquire)
        monkeypatch.setattr(mock_document_persistence_port, "save", mock_fake_save)

        result = fetch_and_store_result.execute(
            DocumentRequest(
                cnpj="12345678912"
            )
        )
        
        assert isinstance(result, FetchAndStoreResult)

        assert result.document_request.cnpj == "12345678912"
        assert result.document_result.document_extracted.supplier.cnpj == "12345678912"
        assert result.document_result.base64_pdf == "BASE64PDF"
        assert result.document_persist_result.result == {"message": "element saved"}

        