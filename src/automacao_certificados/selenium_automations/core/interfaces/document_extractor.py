from typing import Any

from abc import ABC, abstractmethod

from datetime import date

from automacao_certificados.selenium_automations.core.models import (
    dto_document,
    dto_supplier
)
from automacao_certificados.selenium_automations.core.exceptions import *

class DocumentExtractorPort(ABC):
    """
    Interface responsible for defining the contract for document extractors.
    """
    @abstractmethod
    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Gets the supplier.

        :returns: the supplier DTO.
        :rtype: dto_supplier.Supplier
        """
        pass

    @abstractmethod
    def get_document_type(self) -> str:
        """
        Gets the document type.

        :returns: the document type.
        :rtype: str
        """
        pass

    @abstractmethod
    def get_expiration_date(self) -> date:
        """
        Gets the expiration date.

        :returns: the expiration date.
        :rtype: date
        """
        pass

    @abstractmethod
    def get_identifier(self) -> str:
        """
        Gets the document identifier.

        :returns: the document identifier.
        :rtype: str
        """
        pass

    def run(self) -> dto_document.DocumentExtracted:
        """
        Runs the document extractor.

        :returns: the document extracted model.
        :rtype: dto_document.DocumentExtracted

        :raises DocumentExtractorException: Raised when any unexpected error occurs during the extraction process.
        """
        try:
            document = dto_document.DocumentExtracted(
                supplier=self.get_supplier(),
                document_type=self.get_document_type(),
                expiration_date=self.get_expiration_date(),
                identifier=self.get_identifier(),
            )
        except Exception as e:
            raise DocumentExtractorException(e)

        return document
        
