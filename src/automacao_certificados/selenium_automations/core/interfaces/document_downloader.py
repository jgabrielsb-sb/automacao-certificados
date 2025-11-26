from abc import ABC, abstractmethod

from typing import Tuple

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.utils import validate_cnpj


class DocumentDownloaderPort(ABC):
    """
    Interface responsible for downloading certificate documents.
    
    This interface defines the contract for classes that download certificate
    documents from various sources. It uses :class:`DocumentDownloaderInput` 
    for input parameters and returns :class:`DocumentDownloaderOutput` with 
    the extracted document data.
    """
    @abstractmethod
    def get_document(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        """
        Downloads the document.
        :param input: the input of the document downloader.
        :type input: DocumentDownloaderInput
        :return: DocumentDownloaderOutput that contains the extracted document and a base64
            string of the file.
        :rtype: DocumentDownloaderOutput
        """
        pass
    
   
    def run(self, input: DocumentDownloaderInput) -> DocumentDownloaderOutput:
        """
        Runs the document downloader.

        :param input: The input parameters for the downloader.
        :type input: DocumentDownloaderInput

        :returns: A structured output containing the document information and the file encoded as a Base64 string.
        :rtype: DocumentDownloaderOutput

        :raises DocumentDownloaderException: Raised when any unexpected error occurs during the download process.
        """
        validate_cnpj(input.cnpj)
        
        try:
            output = self.get_document(input)
            return output
        except Exception as e:
            raise DocumentDownloaderException(e)

        
        

            