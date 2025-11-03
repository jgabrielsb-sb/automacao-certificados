from automacao_certificados.selenium_automations.core.interfaces import BaseDocumentExtractor
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier
)
from .exceptions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from datetime import date, datetime

class CertificadoCaixaExtractor(BaseDocumentExtractor):
    """
    Extractor for the Certificado Caixa.
    """
    def __init__(
        self, 
        driver: WebDriver,
    ):
        if not isinstance(driver, WebDriver):
            raise ValueError("driver must be a WebDriver")

        self.driver = driver

    def _get_supplier_name(self) -> str:
        """
        Gets the supplier name.
        """
        try:
            razao_social = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH, 
                        "//strong[normalize-space()='Razão Social:']/ancestor::td/following-sibling::td//span[@class='valor']")
                )
            ).text.strip()
            return razao_social
        except Exception as e:
            raise ErrorExtractingDataException("razao_social", e)

    def _get_supplier_cnpj(self) -> str:
        """
        Gets the supplier CNPJ.
        """
        try:
            cnpj = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH, 
                        "//tr[.//strong[normalize-space()='Inscrição:']]//span[@class='valor']")
                )
            ).text.strip()
            return cnpj
        except Exception as e:
            raise ErrorExtractingDataException("cnpj", e)

    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Gets the supplier.
        """
        supplier_name = self._get_supplier_name()
        supplier_cnpj = self._get_supplier_cnpj()
        
        return dto_supplier.Supplier(
            name=supplier_name,
            cnpj=supplier_cnpj,
        )

    def get_document_type(self) -> str:
        """
        Gets the document type.
        """
        return "CERTIFICADO CAIXA"

    def get_identifier(self) -> str:
        """
        Gets the document identifier (Certificação Número).
        """
        try:
            identifier = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//strong[contains(normalize-space(),'Certificação Número')]/following-sibling::span[@class='valor']")
                )
            ).text.strip()
            return identifier
        except Exception as e:
            raise ErrorExtractingDataException("identifier", e)

    def get_expiration_date(self) -> date:
        """
        Gets the expiration date.
        """
        import re

        try:
            # Get full text of the <font> that contains "Validade:" and strip the label
            validade_full = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH, 
                        "//strong[normalize-space()='Validade:']/parent::font"
                    )
                )
            ).text

            # validade_full like: "Validade:02/11/2025 a 01/12/2025"
            validade = validade_full.split("Validade:", 1)[-1].strip()

            # (Optional) split validade into start/end dates:
            datas = re.findall(r"\d{2}/\d{2}/\d{4}", validade)
            validade_inicio, validade_fim = (datas + [None, None])[:2]
            return datetime.strptime(validade_fim, "%d/%m/%Y")
        except Exception as e:
            raise ErrorExtractingDataException("expiration_date", e)

    



    

    