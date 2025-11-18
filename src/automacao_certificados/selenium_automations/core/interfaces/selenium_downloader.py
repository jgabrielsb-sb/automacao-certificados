from abc import ABC, abstractmethod

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from automacao_certificados.selenium_automations.core.models import (
    dto_document
)

from automacao_certificados.selenium_automations.utils import validate_cnpj

class SeleniumDocumentDownloaderPort(ABC):
    """
    Interface responsible for aggregate selenium steps
    and extraction logic to get the document file as a 
    base64 string and the extracted informations.
    """
    def __init__(self, driver: WebDriver):
        if not isinstance(driver, WebDriver):
            raise ValueError('driver must be a Webdriver')

        self.driver = driver

    @abstractmethod
    def get_document(self, cnpj) -> Tuple[dto_document.DocumentExtracted,str]:
        """
        Method to be implemented by child classes.
        Args:
            cnpj: the cnpj of the company.
        Returns:
            Tuple that contains the extracted document and a base64
            string of the file.
        """
        pass
    
   
    def run(self, cnpj: str) -> Tuple[dto_document.DocumentExtracted,str]:
        validate_cnpj(cnpj)
        document_extracted, base64_pdf = self.get_document(cnpj)

        if not isinstance(document_extracted, dto_document.DocumentExtracted):
            raise ValueError("document_extracted must be a dto_document.DocumentExtracted")

        if not isinstance(base64_pdf, str):
            raise ValueError("base64_pdf must a str")

        return document_extracted, base64_pdf

            