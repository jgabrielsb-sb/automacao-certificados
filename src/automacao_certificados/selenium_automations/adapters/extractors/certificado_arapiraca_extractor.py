from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

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


class CertidaoArapiracaExtractor(DocumentExtractorPort):
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
        return "Certidão Negativa Municipal"

    def get_identifier(self) -> str | None:
        """
        Extract the certificate identifier/number.
        The identifier is the "Identificação" or "Inscrição Geral" number (e.g., 491441535).
        """
        try:
            text = self._get_text_from_html()

            # Pattern 1: "Identificação: 491441535" (primary identifier)
            pattern1 = r"Identificação\s*:?\s*(\d+)"
            match = re.search(pattern1, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

            # Pattern 2: "Inscrição Geral: 491441535" (fallback - same value)
            pattern2 = r"Inscrição\s+Geral\s*:?\s*(\d+)"
            match = re.search(pattern2, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

            # Pattern 3: "N.º 41925 / 2025" (certificate number - secondary option)
            pattern3 = r"CERTIDÃO\s+NEGATIVA\s+DE\s+DEBITOS.*?N\.?[º°]\s*(\d+\s*/\s*\d{4})"
            match = re.search(pattern3, text, re.IGNORECASE | re.MULTILINE)
            if match:
                identifier = match.group(1).strip()
                identifier = re.sub(r"\s+", " ", identifier)
                return identifier

            # Pattern 4: "N.° De Autenticidade: 542.F1F.465.99D" (authentication code - last resort)
            pattern4 = r"N\.?[º°]\s*De\s+Autenticidade\s*:?\s*([A-Z0-9\.\-]+)"
            match = re.search(pattern4, text, re.IGNORECASE | re.MULTILINE)
            if match:
                identifier = match.group(1).strip()
                return identifier

            return None

        except Exception as exc:
            raise ErrorExtractingDataException("identifier", exc)

    def get_expiration_date(self) -> date | None:
        """
        Extract the expiration date of the certificate.
        The date appears as "Validade: 12/01/2026" in the HTML.
        Works with both plain text and HTML with nested tags.
        """
        try:
            # First, try to extract from raw HTML to handle nested spans
            html_content = self._html_content
            
            # Pattern to match "Validade:" followed by date, even with HTML tags in between
            # This handles cases like: <strong>Validade:</strong><span><strong>12/01/2026</strong></span>
            # Try multiple patterns to handle different HTML structures
            html_patterns = [
                # Pattern 1: Validade followed by any characters and tags, then date
                r"Validade.*?(\d{2}/\d{2}/\d{4})",
                # Pattern 2: More specific - Validade, then skip tags
                r"Validade[^<]*<[^>]*>[^<]*<[^>]*>[^<]*<[^>]*>(\d{2}/\d{2}/\d{4})",
                # Pattern 3: Validade in tag, then date in next tag content
                r"Validade[^>]*>([^<]*\d{2}/\d{2}/\d{4})",
            ]
            
            for html_pattern in html_patterns:
                match = re.search(html_pattern, html_content, re.IGNORECASE | re.DOTALL)
                if match:
                    date_str = match.group(1)
                    # Clean up the date string (remove any extra characters)
                    date_str = re.search(r'(\d{2}/\d{2}/\d{4})', date_str).group(1)
                    return datetime.strptime(date_str, "%d/%m/%Y").date()
            
            # Fallback: try with extracted text
            text = self._get_text_from_html()
            
            # Pattern to match "Validade:" followed by the date in plain text
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

            # Last fallback: try to find any date in DD/MM/YYYY format
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