# from typing import Protocol, runtime_checkable

# from pydantic import BaseModel

# from automacao_certificados.selenium_automations.core.models import dto_document

# class DocumentPersist(BaseModel):
#     document_extracted: dto_document.DocumentExtracted
#     base64_pdf: str

# class DocumentPersistResult(BaseModel):
#     result: dict | str # should be passed the response of the api, for example.

# @runtime_checkable
# class DocumentPersistancePort(Protocol):
#     def save(self, document: DocumentPersist) -> DocumentPersistResult: ...

from abc import ABC, abstractmethod

from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class DocumentPersistancePort(ABC):
    """
    Interface responsible for save the document.
    """
    @abstractmethod
    def _save(self, input: DocumentPersistanceInput):
        pass

    def run(self, input: DocumentPersistanceInput):
        try:
            self._save(input)
        except Exception as e:
            raise DocumentPersistanceException(e)
