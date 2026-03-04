from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class DocumentPersistancePort(ABC):
    """
    Interface responsible for defining the contract for document persistances.
    """
    @abstractmethod
    def save(self, input: DocumentPersistanceInput) -> DocumentPersistanceOutput:
        """
        Saves the document.

        :param input: the input of the document persistance.
        :type input: DocumentPersistanceInput
        :return:result of the persistance.
        :rtype: DocumentPersistanceOutput
        """
        pass

    def run(self, input: DocumentPersistanceInput) -> DocumentPersistanceOutput:
        """
        Runs the document persistance.

        :param input: the input of the document persistance.
        :type input: DocumentPersistanceInput
        :return: result of the persistance.
        :rtype: DocumentPersistanceOutput
        """
        try:
            return self.save(input)
        except Exception as e:
            raise DocumentPersistanceException("Document Persistance failed: " + str(e))
