from automacao_certificados.selenium_automations.core.interfaces import BaseDocumentExtractor
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier
)
from .exceptions import *

from pathlib import Path
from datetime import date, datetime
import re
import pdfplumber

class CertificadoMaceioExtractor(BaseDocumentExtractor):
    """
    Extractor for the Certificado Municipal Maceió (PDF format).
    """
    def __init__(
        self, 
        pdf_path: str | Path,
    ):
        """
        Initializes the extractor with the PDF file path.
        
        Args:
            pdf_path: Path to the PDF file to extract data from.
        """
        if not isinstance(pdf_path, Path):
            raise ValueError("pdf_path must be a Path object")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
            
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        
        self.pdf_path = pdf_path
        self._pdf_text = None

    def _load_pdf_text(self) -> str:
        """
        Loads and extracts text from the PDF file.
        
        Returns:
            The extracted text from all pages.
        """
        if self._pdf_text is not None:
            return self._pdf_text
        
        with pdfplumber.open(self.pdf_path) as pdf:
            self._pdf_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        return self._pdf_text

    def _get_supplier_name(self) -> str:
        """
        Gets the supplier name (Razão Social) from the PDF.
        """
        try:
            text = self._load_pdf_text()
            
            # Common patterns for supplier name in Brazilian certificates
            patterns = [
                r"(?:Razão Social|Razão\s+Social|Nome\s+Empresarial)[:\s]*([^\n]+)",
                r"(?:Nome\s+da\s+Empresa|Empresa)[:\s]*([^\n]+)",
                r"CNPJ[:\s]*\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}[^\n]*\n([^\n]+)",  # After CNPJ line
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    # Clean up common PDF artifacts
                    name = re.sub(r'\s+', ' ', name)
                    if name and len(name) > 3:  # Basic validation
                        return name
        except Exception as e:
            raise ErrorExtractingDataException(
                "supplier_name", 
                e
            )
        
    def _get_supplier_cnpj(self) -> str:
        """
        Gets the supplier CNPJ from the PDF.
        """
        try:
            text = self._load_pdf_text()
            
            # Pattern for CNPJ: XX.XXX.XXX/XXXX-XX
            cnpj_pattern = r'\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b'
            
            matches = re.findall(cnpj_pattern, text)
            if matches:
                # Usually the first CNPJ found is the company's CNPJ
                # You might want to add logic to find the specific CNPJ if there are multiple
                cnpj = matches[0]
                return cnpj
            
            
        except Exception as e:
            raise ErrorExtractingDataException(
                "cnpj", 
                e
            )

    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Gets the supplier.
        """
        return dto_supplier.Supplier(
            cnpj=self._get_supplier_cnpj(),
        )

    def get_document_type(self) -> str:
        """
        Gets the document type.
        """
        return "CERTIDAO MUNICIPAL MACEIO"

    def get_identifier(self) -> str:
        """
        Gets the document identifier (certificate number).
        Format expected: 0.998.062/25-12 (protocol number format)
        """
        try:
            text = self._load_pdf_text()
            
            # Pattern for protocol number format: X.XXX.XXX/XX-XX (e.g., 0.998.062/25-12)
            protocol_pattern = r'\b(\d+\.\d+\.\d+/\d{2}-\d{2})\b'
            
            # First, try to find protocol number format
            match = re.search(protocol_pattern, text)
            if match:
                identifier = match.group(1).strip()
                if identifier:
                    return identifier
            
            # Common patterns for certificate/identifier numbers with labels
            patterns = [
                r"(?:Número|Nº|Numero|Certificado)[\s:]*([A-Z0-9\./\-]+)",
                r"(?:Protocolo|Protocolo\s+Número)[\s:]*([A-Z0-9\./\-]+)",
                r"(?:Código|Código\s+da\s+Certidão)[\s:]*([A-Z0-9\./\-]+)",
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    identifier = match.group(1).strip()
                    if identifier:
                        return identifier
            
        except Exception as e:
            raise ErrorExtractingDataException(
                "identifier", 
                e
            )

    def get_expiration_date(self) -> date:
        """
        Gets the expiration date.
        """
        try:
            text = self._load_pdf_text()
            
            # Common patterns for expiration date in Brazilian certificates
            patterns = [
                r"(?:Válida\s+até|Válido\s+até|Validade|Vencimento)[\s:]*(\d{2}/\d{2}/\d{4})",
                r"(?:Expira\s+em|Expiração)[\s:]*(\d{2}/\d{2}/\d{4})",
                r"(\d{2}/\d{2}/\d{4})\s+(?:a|até)\s+(\d{2}/\d{2}/\d{4})",  # Date range, take the end date
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    if len(match.groups()) == 2:  # Date range pattern
                        expiration_date_str = match.group(2)  # Take the end date
                    else:
                        expiration_date_str = match.group(1)
                    
                    expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y").date()
                    return expiration_date
            
            # Fallback: look for any date pattern and try to find the latest one
            date_pattern = r'\b(\d{2}/\d{2}/\d{4})\b'
            dates = re.findall(date_pattern, text)
            if dates:
                # Try to parse dates and find the one that's likely the expiration date
                # Usually the expiration date is one of the later dates in the document
                parsed_dates = []
                for date_str in dates:
                    try:
                        parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                        parsed_dates.append(parsed_date)
                    except ValueError:
                        continue
                
                if parsed_dates:
                    # Return the latest date (often the expiration date)
                    return max(parsed_dates)
            
        except Exception as e:
            raise ErrorExtractingDataException(
                "expiration_date", 
                e
            )

