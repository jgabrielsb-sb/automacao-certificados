from typing import Any

from abc import ABC, abstractmethod

from datetime import date

from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier
)

class BaseDocumentExtractor(ABC):
    """
    Base class for all extractors.
    """
    @abstractmethod
    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Gets the supplier.
        """
        pass

    @abstractmethod
    def get_document_type(self) -> str:
        """
        Gets the document type.
        """
        pass

    @abstractmethod
    def get_expiration_date(self) -> date:
        """
        Gets the expiration date.
        """
        pass

    def run(self) -> dto_document.DocumentExtracted:
        """
        Runs the document extractor.
        Args:
            None
        Returns:
            The document extracted model.
        """
        document = dto_document.DocumentExtracted(
            supplier=self.get_supplier(),
            document_type=self.get_document_type(),
            expiration_date=self.get_expiration_date(),
        )
        return document
        
