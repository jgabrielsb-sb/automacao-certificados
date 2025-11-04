from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester
from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import *
from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier,
)

from .exceptions import *

class RegisterDocumentService:
    """
    Service Layer that handles the registration of a document.
    """
    def __init__(
        self,
        api_requester: BaseAPIRequester
    ):
        self.api_requester = api_requester

    def _get_or_create_supplier(
        self,
        supplier: dto_supplier.SupplierCreate
    ) -> dto_supplier.SupplierResponse:  
        """
        Get the supplier or create it if not registered yet.
        Arguments:
            supplier: the supplier to get or create
        Returns:
            the supplier.
        """
        try:
            return self.api_requester.get_supplier(
                dto_supplier.SupplierFilter(cnpj=supplier.cnpj)
            )[0]
        except NotFoundError:
            return self.api_requester.register_supplier(
                dto_supplier.SupplierCreate(cnpj=supplier.cnpj)
            )

    def run(
        self,
        base64_encoded_pdf: str,
        document_extracted: dto_document.DocumentExtracted
    ) -> dto_document.DocumentResponse:
        """
        Register a document by:
            - getting or creating the supplier;
            - getting the document type;
            - registering the document with the respective ids.
        Arguments:
            base64_encoded_pdf: a encoded base 64 of the pdf
            document_extracted: the extracted document
        Returns:
            The created document
        Raises:
            DocumentTypeNotFoundError: if the document could not be created
            because the document type is not accepted/created on the database.
        """
        
        # 1. Get or register supplier
        supplier = self._get_or_create_supplier(document_extracted.supplier)

        # 2. Get document type: raise NotFoundError if document type not found
        try:
            document_type = self.api_requester.get_document_type(document_extracted.document_type)
        except NotFoundError as e:
            raise DocumentTypeNotFoundError(
                message=f"Document Type not found on API: {document_extracted.document_type}. You must register it first."
            )
        
        document_create = dto_document.DocumentCreate(
            supplier_id=supplier.id,
            document_type_id=document_type.id,
            identifier=document_extracted.identifier,
            expiration_date=document_extracted.expiration_date,
        )

        document_response = self.api_requester.register_document(document_create)
        return document_response