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
    def _get_document(self, input: DocumentDownloaderInput) -> Tuple[dto_document.DocumentExtracted, str]:
        """
        Method to be implemented by child classes.
        Args:
            input: the input of the document downloader.
        Returns:
            Tuple that contains the extracted document and a base64
            string of the file.
        """
        pass
    
   
    def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        validate_cnpj(input.cnpj)
        
        try:
            document_extracted, base64_pdf = self._get_document(input)
            return DocumentDownloaderOutput(
                document_extracted=document_extracted,
                base64_pdf=base64_pdf
            )
        except Exception as e:
            raise DocumentDownloaderException(e)

        
        

            