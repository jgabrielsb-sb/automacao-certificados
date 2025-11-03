from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document
)

class BaseAPIRequester(ABC):
    """
    Base class for all API requesters.
    """
    @abstractmethod
    def register_supplier(
        self, 
        supplier: dto_supplier.SupplierCreate
    ) -> dto_supplier.SupplierResponse:
        """
        Registers a supplier.
        Method to be implemented by the child classes.
        Args:
            supplier: The supplier to register.
        Returns:
            The supplier response.
        """
        pass

    @abstractmethod
    def get_supplier(
        self, 
        filter: dto_supplier.SupplierFilter
    ) -> list[dto_supplier.SupplierResponse]:
        """
        Gets a supplier by filter.
        Method to be implemented by the child classes.
        Args:
            filter: The filter to get the supplier.
        Returns:
            The supplier response.
        """
        pass

    @abstractmethod
    def register_document(
        self,
        document: dto_document.DocumentCreate
    ) -> dto_document.DocumentResponse:
        """
        Registers a document.
        Method to be implemented by the child classes.
        Args:
            document: The document to register.
        Returns:
            The document response.
        """
        pass

    @abstractmethod
    def get_document(
        self,
        filter: dto_document.DocumentFilter
    ) -> list[dto_document.DocumentResponse]:
        """
        Gets a document by filter.
        Method to be implemented by the child classes.
        """
        pass

        

    