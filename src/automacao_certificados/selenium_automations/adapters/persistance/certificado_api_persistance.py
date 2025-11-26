# adapters/persistence/api_persistence.py
from automacao_certificados.selenium_automations.core.interfaces import DocumentPersistancePort

from automacao_certificados.selenium_automations.core.models import (
    SupplierCreate, 
    SupplierResponse, 
    SupplierFilter,
    DocumentCreate,
    DocumentTypeFilter,
    DocumentPersistanceInput,
    DocumentPersistanceOutput,
)
    

from automacao_certificados.selenium_automations.core.exceptions import *

from automacao_certificados.selenium_automations.infra.api_requester import CertificadoAPIRequester

class CertificadoApiPersistance(DocumentPersistancePort):
    def __init__(self, api_requester: CertificadoAPIRequester):
        """
        The certificado api persistance is an implementation of the document persistance port 
        that uses the certificado api to persist the document.
        """
        if not isinstance(api_requester, CertificadoAPIRequester):
            raise ValueError("api_requester must be a CertificadoAPIRequester")

        super().__init__()

        self.api_requester = api_requester

    def get_or_create_supplier(
        self,
        supplier: SupplierCreate
    ) -> SupplierResponse:
        """
        Gets the supplier by cnpj using the certificado api or creates a new one if it doesn't exist.

        :param supplier: The supplier to get or create.
        :type supplier: SupplierCreate
        :return: The supplier response.
        :rtype: SupplierResponse
        """
        try:
            return self.api_requester.get_supplier(
                SupplierFilter(cnpj=supplier.cnpj)
            )[0]
        except NotFoundError:
            return self.api_requester.register_supplier(
                SupplierCreate(cnpj=supplier.cnpj)
            )

    def save(self, input: DocumentPersistanceInput):
        """
        Saves the document on database using the certificado api.

        :param input: The input of the document persistance.
        :type input: DocumentPersistanceInput
        :return: The document persistance output.
        :rtype: DocumentPersistanceOutput
        :raises DocumentTypeNotFoundError: If the document type is not found.
        """
        supplier_create = SupplierCreate(**input.document_extracted.supplier.model_dump())
        
        # 1) Supplier
        supplier_resp = self.get_or_create_supplier(supplier_create)

        # 2) Doc type
        try:
            doc_type_resp = self.api_requester.get_document_type(
                DocumentTypeFilter(
                    name=input.document_extracted.document_type
                )
            )[0]
        except NotFoundError:
            # You can raise a domain-specific error or map it
            raise DocumentTypeNotFoundError(
                message=f"Document Type not found on API: {input.document_extracted.document_type}. Register it first."
            )

        # 3) Register document metadata
        document_create = DocumentCreate(
            supplier_id=supplier_resp.id,
            document_type_id=doc_type_resp.id,
            identifier=input.document_extracted.identifier,
            expiration_date=input.document_extracted.expiration_date,
            base64_pdf=input.base64_pdf
        )
        
        created = self.api_requester.register_document(document=document_create)        

        return DocumentPersistanceOutput(result=created.model_dump(mode="json"))