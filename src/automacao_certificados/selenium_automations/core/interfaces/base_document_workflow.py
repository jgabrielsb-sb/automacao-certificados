from abc import ABC, abstractmethod

from typing import Tuple

from pathlib import Path

from automacao_certificados.selenium_automations.core.models import (
    dto_document,
)

from automacao_certificados.selenium_automations.core.interfaces.base_api_requester import BaseAPIRequester

class BaseDocumentWorkflow(ABC):

    def __init__(
        self,
    ):
    
    @abstractmethod
    def _get_document(self) -> Tuple[str, dto_document.DocumentExtracted]:
        """
        Method to be implemented by the child classes.
        Must return a tuple with:
        - A base64 encoded pdf file
        - A document extracted model
        """
        pass

    def get_document(self) -> Tuple[str, dto_document.DocumentExtracted]:
        base64_encoded_pdf, document_extracted = self._get_document()
        
        if not isinstance(base64_encoded_pdf, str):
            raise ValueError("base64_encoded_pdf must be a string")
        
        if not isinstance(document_extracted, dto_document.DocumentExtracted):
            raise ValueError("document_extracted must be a dto_document.DocumentExtracted object")
        
        return base64_encoded_pdf, document_extracted

    @abstractmethod
    def save_document(
        self, 
        base64_encoded_pdf: str, 
        document_extracted: dto_document.DocumentExtracted
    ) -> None:

    def run(self) -> Tuple[str, dto_document.DocumentExtracted]:
        """
        Runs the document workflow.
        """
        return self._get_document()