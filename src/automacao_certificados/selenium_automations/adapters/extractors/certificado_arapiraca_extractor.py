from automacao_certificados.selenium_automations.core.interfaces import BaseDocumentExtractor
from automacao_certificados.selenium_automations.core.models import dto_supplier
from .exceptions import *

from datetime import datetime, date
import re
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Helper class to extract text from HTML."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style'}
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag.lower()
    
    def handle_endtag(self, tag):
        self.current_tag = None
    
    def handle_data(self, data):
        if self.current_tag not in self.ignore_tags:
            self.text_parts.append(data)
    
    def get_text(self) -> str:
        return ' '.join(self.text_parts)


class CertidaoArapiracaExtractor(BaseDocumentExtractor):
    """
    Extractor for the Certidão Municipal de Arapiraca.
    Accepts HTML content as a string.
    """

    def __init__(self, html_content: str):
        """
        Args:
            html_content (str): HTML content of the certificate page.
        """
        if not isinstance(html_content, str):
            raise ValueError("html_content must be a string")

        if not html_content.strip():
            raise ValueError("html_content string is empty")

        self._html_content = html_content
        self._html_text: str | None = None

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _get_text_from_html(self) -> str:
        """
        Extract text from HTML content.
        """
        if self._html_text is not None:
            return self._html_text

        parser = HTMLTextExtractor()
        parser.feed(self._html_content)
        self._html_text = parser.get_text()
        
        return self._html_text

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------

    def _get_supplier_cnpj(self) -> str | None:
        """
        Extract the CNPJ from the HTML text.
        """
        try:
            text = self._get_text_from_html()

            # Pattern to match CNPJ/CPF field
            # Look for "CNPJ/CPF:" followed by the CNPJ
            cnpj_pattern = r"CNPJ/CPF\s*:?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})"
            match = re.search(cnpj_pattern, text, re.IGNORECASE)

            if match:
                return match.group(1)

            # Fallback: try to find any CNPJ pattern
            cnpj_pattern_fallback = r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b"
            match = re.search(cnpj_pattern_fallback, text)
            
            return match.group(1) if match else None

        except Exception as exc:
            raise ErrorExtractingDataException("cnpj", exc)

    def _get_supplier_name(self) -> str | None:
        """
        Extract the supplier name from the HTML text.
        """
        try:
            text = self._get_text_from_html()

            # Pattern to match "Contribuinte:" followed by the name
            pattern = r"Contribuinte\s*:?\s*([^\n]+?)(?:\s+CNPJ|$)"
            match = re.search(pattern, text, re.IGNORECASE)
            
            if match:
                name = match.group(1).strip()
                # Clean up the name
                name = re.sub(r"\s+", " ", name)
                return name if name else None

            return None

        except Exception as exc:
            raise ErrorExtractingDataException("supplier_name", exc)

    # ------------------------------------------------------------------
    # Public API required by BaseDocumentExtractor
    # ------------------------------------------------------------------

    def get_supplier(self) -> dto_supplier.Supplier:
        """
        Returns the supplier DTO.
        """
        return dto_supplier.Supplier(
            cnpj=self._get_supplier_cnpj(),
        )

    def get_document_type(self) -> str:
        """
        Returns the document type.
        """
        return "CERTIDAO MUNICIPAL ARAPIRACA"

    def get_identifier(self) -> str | None:
        """
        Extract the certificate identifier/number.
        """
        try:
            text = self._get_text_from_html()

            # Try to find "N.º" or "N.°" followed by the certificate number
            # Pattern 1: "N.º 41925 / 2025" (certificate number)
            pattern1 = r"CERTIDÃO\s+NEGATIVA\s+DE\s+DEBITOS.*?N\.?[º°]\s*(\d+\s*/\s*\d{4})"
            match = re.search(pattern1, text, re.IGNORECASE | re.MULTILINE)
            if match:
                identifier = match.group(1).strip()
                identifier = re.sub(r"\s+", " ", identifier)
                return identifier

            # Pattern 2: "N.° De Autenticidade: 542.F1F.465.99D" (authentication code)
            pattern2 = r"N\.?[º°]\s*De\s+Autenticidade\s*:?\s*([A-Z0-9\.\-]+)"
            match = re.search(pattern2, text, re.IGNORECASE | re.MULTILINE)
            if match:
                identifier = match.group(1).strip()
                return identifier

            # Pattern 3: Generic "N.º" or "Número" pattern
            pattern3 = r"(?:Número|Numero|N\.?[º°])\s*:?\s*(\d+\s*/\s*\d{4})"
            match = re.search(pattern3, text, re.IGNORECASE | re.MULTILINE)
            if match:
                identifier = match.group(1).strip()
                identifier = re.sub(r"\s+", " ", identifier)
                return identifier

            return None

        except Exception as exc:
            raise ErrorExtractingDataException("identifier", exc)

    def get_expiration_date(self) -> date | None:
        """
        Extract the expiration date of the certificate.
        The date appears as "Validade: 12/01/2026" in the HTML.
        """
        try:
            text = self._get_text_from_html()

            # Pattern to match "Validade:" followed by the date
            # This is the most common format in Arapiraca certificates
            patterns = [
                r"Validade\s*:?\s*(\d{2}/\d{2}/\d{4})",
                r"(?:Válida\s+até|Válido\s+até|Vencimento)\s*:?\s*(\d{2}/\d{2}/\d{4})",
                r"(?:Expira\s+em|Expiração)\s*:?\s*(\d{2}/\d{2}/\d{4})",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    date_str = match.group(1)
                    return datetime.strptime(date_str, "%d/%m/%Y").date()

            # Fallback: try to find any date in DD/MM/YYYY format
            date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"
            all_dates = re.findall(date_pattern, text)

            if all_dates:
                parsed = []
                for d in all_dates:
                    try:
                        parsed.append(datetime.strptime(d, "%d/%m/%Y").date())
                    except ValueError:
                        continue
                if parsed:
                    # Return the latest date (likely the expiration date)
                    return max(parsed)

            return None

        except Exception as exc:
            raise ErrorExtractingDataException("expiration_date", exc)