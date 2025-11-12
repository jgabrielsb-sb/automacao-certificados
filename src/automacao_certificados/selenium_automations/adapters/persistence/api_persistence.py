# adapters/persistence/api_persistence.py
from automacao_certificados.selenium_automations.core.interfaces import (
    DocumentPersistancePort, DocumentPersist, DocumentPersistResult
)
from automacao_certificados.selenium_automations.core.models import (
    dto_document, 
    dto_supplier,
    dto_document_type,
)
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import  *
from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester
from .exceptions import *

class ApiPersistence(DocumentPersistancePort):
    """
    Hexagonal adapter: implements DocumentPersistencePort by delegating to the
    API via BaseAPIRequester. This is essentially your RegisterDocumentService,
    but conforming to the port interface.
    """
    def __init__(self, api_requester: BaseAPIRequester):
        self.api_requester = api_requester

    def _get_or_create_supplier(
        self,
        supplier: dto_supplier.SupplierCreate
    ) -> dto_supplier.SupplierResponse:
        try:
            return self.api_requester.get_supplier(
                dto_supplier.SupplierFilter(cnpj=supplier.cnpj)
            )[0]
        except NotFoundError:
            return self.api_requester.register_supplier(
                dto_supplier.SupplierCreate(cnpj=supplier.cnpj)
            )

    def save(self, doc: DocumentPersist) -> DocumentPersistResult:
        supplier_create = dto_supplier.SupplierCreate(**doc.document_extracted.supplier.model_dump())
        
        # 1) Supplier
        supplier_resp = self._get_or_create_supplier(supplier_create)

        # 2) Doc type
        try:
            doc_type_resp = self.api_requester.get_document_type(
                dto_document_type.DocumentTypeFilter(
                    name=doc.document_extracted.document_type
                )
            )[0]
        except NotFoundError:
            # You can raise a domain-specific error or map it
            raise DocumentTypeNotFoundError(
                message=f"Document Type not found on API: {doc.document_extracted.document_type}. Register it first."
            )

        # 3) Register document metadata
        document_create = dto_document.DocumentCreate(
            supplier_id=supplier_resp.id,
            document_type_id=doc_type_resp.id,
            identifier=doc.document_extracted.identifier,
            expiration_date=doc.document_extracted.expiration_date,
            base64_pdf=doc.base64_pdf
        )
        
        created = self.api_requester.register_document(document_create)        

        return DocumentPersistResult(result=created.model_dump(mode="json"))