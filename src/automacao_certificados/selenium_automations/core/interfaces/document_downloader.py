from abc import ABC, abstractmethod

from typing import Tuple

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.utils import validate_cnpj


class DocumentDownloaderPort(ABC):
    """
    Interface responsible for aggregate selenium steps
    and extraction logic to get the document file as a 
    base64 string and the extracted informations.
    """
    @abstractmethod
    def _get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        """
        Method to be implemented by child classes.
        Args:
            input: the input of the document downloader.
        Returns:
            DocumentDownloaderOutput that contains the extracted document and a base64
            string of the file.
        """
        pass
    
   
    def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        validate_cnpj(input.cnpj)
        
        try:
            output = self._get_document(input)
            return output
        except Exception as e:
            raise DocumentDownloaderException(e)

        
        

            