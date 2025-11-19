from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class DocumentPersistancePort(ABC):
    """
    Interface responsible for save the document.
    """
    @abstractmethod
    def _save(self, input: DocumentPersistanceInput) -> DocumentPersistanceOutput:
        pass

    def run(self, input: DocumentPersistanceInput) -> DocumentPersistanceOutput:
        try:
            return self._save(input)
        except Exception as e:
            raise DocumentPersistanceException(e)
