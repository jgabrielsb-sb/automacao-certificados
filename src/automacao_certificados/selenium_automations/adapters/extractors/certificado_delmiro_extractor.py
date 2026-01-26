from automacao_certificados.selenium_automations.core.interfaces import DocumentExtractorPort
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from datetime import date, datetime
import re


class CertificadoDelmiroExtractor(DocumentExtractorPort):
    """
    Extractor for the Certidão Negativa de Débitos from Delmiro Gouveia.
    """
    def __init__(
        self, 
        driver: WebDriver,
    ):
        """
        The certificado delmiro extractor is an implementation of the document extractor port 
        that uses a web driver to extract the document.
        """
        if not isinstance(driver, WebDriver):
            raise ValueError("driver must be a WebDriver")

        self.driver = driver

    def _get_supplier_name(self) -> str:
        """
        Gets the supplier name (Nome do econômico or Nome empresarial).

        :return: The supplier name.
        :rtype: str
        """
        try:
            # Try multiple XPath patterns to find the supplier name
            patterns = [
                # Pattern 1: "Nome do econômico:" in one cell, value in next cell (handles nested elements)
                "//td[contains(., 'Nome do econômico:')]/following-sibling::td",
                # Pattern 2: "Nome do econômico:" in same cell, extract after colon (handles nested elements)
                "//td[contains(., 'Nome do econômico:')]",
                # Pattern 3: "Nome empresarial:" in one cell, value in next cell (handles nested elements)
                "//td[contains(., 'Nome empresarial:')]/following-sibling::td",
                # Pattern 4: "Nome empresarial:" in same cell, extract after colon (handles nested elements)
                "//td[contains(., 'Nome empresarial:')]",
            ]
            
            for pattern in patterns:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, pattern))
                    )
                    text = element.text.strip()
                    
                    # If the text contains the label, extract the value after the colon
                    if ':' in text:
                        text = text.split(':', 1)[-1].strip()
                    
                    if text:
                        return text
                except:
                    continue
            
            raise ValueError("Could not find supplier name")
        except Exception as e:
            raise ErrorExtractingDataException("supplier_name", e)

    def _get_supplier_cnpj(self) -> str:
        """
        Gets the supplier CNPJ.

        :return: The supplier CNPJ.
        :rtype: str
        """
        try:
            # Try multiple XPath patterns to find the CNPJ
            patterns = [
                # Pattern 1: "CPF/CNPJ:" in one cell, value in next cell (handles nested elements)
                "//td[contains(., 'CPF/CNPJ:')]/following-sibling::td",
                # Pattern 2: "CPF/CNPJ:" in same cell, extract after colon (handles nested elements)
                "//td[contains(., 'CPF/CNPJ:')]",
            ]
            
            for pattern in patterns:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, pattern))
                    )
                    text = element.text.strip()
                    
                    # If the text contains the label, extract the value after the colon
                    if ':' in text:
                        text = text.split(':', 1)[-1].strip()
                    
                    # Clean the CNPJ (remove any extra spaces or formatting)
                    cnpj = re.sub(r'\s+', '', text)
                    if cnpj:
                        return cnpj
                except:
                    continue
            
            raise ValueError("Could not find CNPJ")
        except Exception as e:
            raise ErrorExtractingDataException("cnpj", e)

    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Gets the supplier.

        :return: The supplier DTO.
        :rtype: dto_supplier.Supplier
        """
        supplier_cnpj = self._get_supplier_cnpj()
        
        return dto_supplier.Supplier(
            cnpj=supplier_cnpj,
        )

    def get_document_type(self) -> str:
        """
        Gets the document type.

        :return: The document type.
        :rtype: str
        """
        return "Certidão Negativa Municipal"

    def get_identifier(self) -> str:
        """
        Gets the document identifier (Número).

        :return: The document identifier.
        :rtype: str
        """
        try:
            # Try multiple XPath patterns to find the identifier
            patterns = [
                # Pattern 1: "Número:" in one cell, value in next cell (handles nested elements)
                "//td[contains(., 'Número:')]/following-sibling::td",
                # Pattern 2: "Número:" in same cell, extract after colon (handles nested elements)
                "//td[contains(., 'Número:')]",
            ]
            
            for pattern in patterns:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, pattern))
                    )
                    text = element.text.strip()
                    
                    # If the text contains the label, extract the value after the colon
                    if ':' in text:
                        text = text.split(':', 1)[-1].strip()
                    
                    if text:
                        return text
                except:
                    continue
            
            raise ValueError("Could not find identifier")
        except Exception as e:
            raise ErrorExtractingDataException("identifier", e)

    def get_expiration_date(self) -> date:
        """
        Gets the expiration date (Validade).

        :return: The expiration date.
        :rtype: date
        """
        try:
            # Try multiple XPath patterns to find the validity date
            patterns = [
                # Pattern 1: "Validade:" in one cell, value in next cell (handles nested elements)
                "//td[contains(., 'Validade:')]/following-sibling::td",
                # Pattern 2: "Validade:" in same cell, extract after colon (handles nested elements)
                "//td[contains(., 'Validade:')]",
            ]
            
            validade_text = None
            for pattern in patterns:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, pattern))
                    )
                    text = element.text.strip()
                    
                    # If the text contains the label, extract the value after the colon
                    if ':' in text:
                        text = text.split(':', 1)[-1].strip()
                    
                    if text:
                        validade_text = text
                        break
                except:
                    continue
            
            if not validade_text:
                raise ValueError("Could not find validity date")

            # Extract date from text (format: DD/MM/YYYY)
            # The validade_text might be like "27/03/2026" or "26/01/2026 a 27/03/2026"
            date_pattern = r'\d{2}/\d{2}/\d{4}'
            dates = re.findall(date_pattern, validade_text)
            
            if dates:
                # If there are two dates, use the last one (expiration date)
                # If there's only one, use it
                expiration_date_str = dates[-1]
                return datetime.strptime(expiration_date_str, "%d/%m/%Y").date()
            else:
                raise ValueError(f"Could not find date pattern in: {validade_text}")
        except Exception as e:
            raise ErrorExtractingDataException("expiration_date", e)
