from automacao_certificados.selenium_automations.adapters.api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier,
    dto_document_type,
)

from automacao_certificados.selenium_automations.adapters.api_requester.exceptions import NotFoundError

class CertificadoAPIService:
    def __init__(
        self, 
        api_requester: CertificadoAPIRequester
    ):
        self.api_requester = api_requester

    def is_supplier_already_registered(self, cnpj: str) -> bool:
        """
        Checks if a supplier is already registered.
        """
        try:
            self.api_requester.get_supplier(
                filter=dto_supplier.SupplierFilter(
                    cnpj=cnpj
                )
            )
            return True
        except NotFoundError:
            return False

    def register_document(
        self,
        document: dto_document.DocumentExtracted
    ) -> dto_document.DocumentResponse:
        """
        Registers a document.
        """
        supplier_cnpj = document.supplier.cnpj

        if not self.is_supplier_already_registered(supplier_cnpj):
            supplier = self.api_requester.register_supplier(
                supplier=dto_supplier.SupplierCreate(
                    cnpj=supplier_cnpj
                )
            )
            supplier_id = supplier.id

        else:
            supplier = self.api_requester.get_supplier(
                filter=dto_supplier.SupplierFilter(
                    cnpj=supplier_cnpj
                )
            )
            supplier_id = supplier[0].id

        document_type = document.document_type

        document_type = self.api_requester.get_document_type(
            filter=dto_document_type.DocumentTypeFilter(
                name=document_type
            )
        )

        document_type_id = document_type[0].id

        document = self.api_requester.register_document(
            document=dto_document.DocumentCreate(
                supplier_id=supplier_id,
                document_type_id=document_type_id,
                identifier=document.identifier,
                expiration_date=document.expiration_date
            )
        )
        return document

        
        
    

    

    
        
    