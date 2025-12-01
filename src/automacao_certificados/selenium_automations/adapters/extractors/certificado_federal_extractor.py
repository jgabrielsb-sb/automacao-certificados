import base64
import pdfplumber
from io import BytesIO
import re
from datetime import datetime, date

from automacao_certificados.selenium_automations.core.interfaces.document_extractor import DocumentExtractorPort
from automacao_certificados.selenium_automations.core.models import Supplier
from automacao_certificados.selenium_automations.core.exceptions import ErrorExtractingDataException

class CertificadoFederalExtractor(DocumentExtractorPort):
    def __init__(self, base64_pdf: str):
        """
        The certificado federal extractor is an implementation of the document extractor port 
        that uses a base64 pdf to extract the document.
        """
        if not isinstance(base64_pdf, str):
            raise ValueError("base64_pdf must be a string")

        if not base64_pdf.strip():
            raise ValueError("base64_pdf string is empty")

        try:
            # Decode BASE64 → raw PDF bytes
            pdf_bytes = base64.b64decode(base64_pdf.encode("ascii"))
        except Exception as exc:
            raise ValueError("Invalid base64 PDF string") from exc

        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("Decoded data is not a valid PDF file")

        self._pdf_bytes = pdf_bytes
        self._pdf_text: str | None = None

    def _load_pdf_text(self) -> str:
        """
        Decode PDF bytes → extract text from ALL pages.

        :return: The pdf text.
        :rtype: str
        """
        if self._pdf_text is not None:
            return self._pdf_text

        with pdfplumber.open(BytesIO(self._pdf_bytes)) as pdf:
            self._pdf_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        return self._pdf_text

    def _get_supplier_cnpj(self) -> str:
        """
        Extract the CNPJ from the PDF text.

        :return: The CNPJ.
        :rtype: str
        """
        try:
            text = self._load_pdf_text()

            # Standard CNPJ pattern: XX.XXX.XXX/XXXX-XX
            cnpj_pattern = r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b"
            match = re.search(cnpj_pattern, text)

            if match:
                return match.group(1)
            
            raise ErrorExtractingDataException("cnpj", ValueError("CNPJ not found in PDF"))

        except ErrorExtractingDataException:
            raise
        except Exception as exc:
            raise ErrorExtractingDataException("cnpj", exc)

    def _get_supplier_name(self) -> str:
        """
        Extract the supplier name from the PDF text.

        :return: The supplier name.
        :rtype: str
        """
        try:
            text = self._load_pdf_text()

            # Get CNPJ first to use as reference point
            cnpj = self._get_supplier_cnpj()
            
            # Patterns to find supplier name in federal certificates
            patterns = [
                # Pattern 1: "Razão Social:" or "Razão Social" followed by name
                r"(?:Razão\s+Social)[:\s]*([^\n]+)",
                # Pattern 2: "Nome Empresarial:" or similar
                r"(?:Nome\s+Empresarial|Nome\s+da\s+Empresa|Empresa)[:\s]*([^\n]+)",
                # Pattern 3: Look for name on the line immediately before CNPJ
                r"([^\n]+)\s*\n\s*CNPJ[:\s]*" + re.escape(cnpj),
                # Pattern 4: Look for name on the line immediately after CNPJ
                r"CNPJ[:\s]*" + re.escape(cnpj) + r"[^\n]*\n\s*([^\n]+)",
                # Pattern 5: Look for name before CNPJ on the same line (with space)
                r"([A-Z][^\n]{3,}?)\s+CNPJ[:\s]*" + re.escape(cnpj),
                # Pattern 6: Look for Brazilian company name format (contains S.A, LTDA, EIRELI, etc.)
                # This pattern looks for uppercase text that contains common Brazilian company suffixes
                r"([A-Z][A-Z\s\.]{2,}(?:S\.A|S\.A\.|LTDA|EIRELI|ME|EPP|SS)[^\n]*)",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    # Clean up whitespace
                    name = re.sub(r"\s+", " ", name)
                    # Remove common prefixes/suffixes that might be captured (including "Nome:" with colon)
                    name = re.sub(r"^(Razão\s+Social|Nome\s+Empresarial|Nome\s*:|Nome|Empresa|CNPJ)[:\s]*", "", name, flags=re.IGNORECASE)
                    # Remove CNPJ if accidentally captured
                    name = re.sub(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", "", name).strip()
                    # Remove trailing periods (S.A. should become S.A)
                    # Replace S.A. with S.A, then remove any remaining trailing periods
                    name = re.sub(r'\bS\.A\.$', 'S.A', name)
                    name = name.rstrip('.,;:')
                    if name and len(name) > 3:  # Basic validation
                        return name

            # Fallback: Look for capitalized text lines near the CNPJ
            # Find the line containing CNPJ
            lines = text.split('\n')
            cnpj_line_idx = None
            for i, line in enumerate(lines):
                if cnpj in line:
                    cnpj_line_idx = i
                    break
            
            if cnpj_line_idx is not None:
                # Check lines before and after CNPJ for potential company name
                # Company names in federal certs are often standalone lines with uppercase letters
                # Priority: check line before CNPJ first (most common location)
                search_indices = [cnpj_line_idx - 1, cnpj_line_idx - 2, cnpj_line_idx + 1, cnpj_line_idx - 3]
                
                for idx in search_indices:
                    if 0 <= idx < len(lines):
                        candidate = lines[idx].strip()
                        # Check if it looks like a company name
                        # Must have uppercase letters, reasonable length, not be a label, not contain CNPJ
                        if (candidate and 
                            len(candidate) >= 3 and 
                            len(candidate) < 200 and
                            re.search(r'[A-Z]', candidate) and
                            not re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', candidate) and
                            not re.match(r'^(CNPJ|Razão|Nome|Empresa|Protocolo|Validade|Válida|Vencimento|Certidão|Data|Emissão)', candidate, re.IGNORECASE) and
                            # Should contain letters (not just numbers/symbols)
                            re.search(r'[A-Za-z]{3,}', candidate)):
                            # Clean up whitespace
                            candidate = re.sub(r"\s+", " ", candidate)
                            # Remove any trailing/leading punctuation that might be artifacts
                            candidate = candidate.strip('.,;:')
                            if candidate:
                                return candidate

            raise ErrorExtractingDataException("supplier_name", ValueError("Supplier name not found in PDF"))

        except ErrorExtractingDataException:
            raise
        except Exception as exc:
            raise ErrorExtractingDataException("supplier_name", exc)

    def get_supplier(self) -> Supplier:
        """
        Get the supplier from the PDF.

        :return: The supplier DTO.
        :rtype: Supplier
        """
        supplier_cnpj = self._get_supplier_cnpj()
        
        return Supplier(
            cnpj=supplier_cnpj,
        )

    def get_document_type(self):
        return "Certidão Negativa Federal"

    def get_identifier(self) -> str | None:
        """
        Extract the certificate identifier/number from the PDF text.
        For federal certificates, this is typically a protocol number or certificate code.

        :return: The identifier, or None if not found.
        :rtype: str | None
        """
        try:
            text = self._load_pdf_text()

            # Patterns to find identifier in federal certificates
            patterns = [
                # Pattern 1: Protocol number format (common in Brazilian certificates)
                r"(?:Protocolo|Protocolo\s+Número|Número\s+do\s+Protocolo)[:\s]*([A-Z0-9\./\-]+)",
                # Pattern 2: Certificate number
                r"(?:Certificado\s+Número|Número\s+da\s+Certidão|Código)[:\s]*([A-Z0-9\./\-]+)",
                # Pattern 3: Standard protocol format: X.XXX.XXX/XXXX-XX
                r"\b(\d+\.\d+\.\d+/\d{4}-\d{2})\b",
                # Pattern 4: Look for "Número" or "Código" followed by alphanumeric
                r"(?:Número|Nº|Numero|Código)[\s:]*([A-Z0-9\./\-]+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    identifier = match.group(1).strip()
                    if identifier:
                        return identifier

            return None

        except Exception as exc:
            raise ErrorExtractingDataException("identifier", exc)

    def get_expiration_date(self) -> date:
        """
        Extract the expiration date from the PDF text.

        :return: The expiration date.
        :rtype: date
        """
        try:
            text = self._load_pdf_text()

            # Patterns to find expiration date in federal certificates
            patterns = [
                # Pattern 1: "Válida até" or "Válido até" followed by date
                r"(?:Válida\s+até|Válido\s+até|Validade|Vencimento)[\s:]*(\d{2}/\d{2}/\d{4})",
                # Pattern 2: "Expira em" or "Expiração" followed by date
                r"(?:Expira\s+em|Expiração)[\s:]*(\d{2}/\d{2}/\d{4})",
                # Pattern 3: Date range format: "DD/MM/YYYY a DD/MM/YYYY" (second date is expiration)
                r"(\d{2}/\d{2}/\d{4})\s+(?:a|até)\s+(\d{2}/\d{2}/\d{4})",
                # Pattern 4: "Vigência" followed by date range
                r"Vigência[:\s]*\d{2}/\d{2}/\d{4}\s+(?:a|até)\s+(\d{2}/\d{2}/\d{4})",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    if len(match.groups()) == 2:
                        # Range: second date = expiration
                        expiration_str = match.group(2)
                    else:
                        expiration_str = match.group(1)

                    return datetime.strptime(expiration_str, "%d/%m/%Y").date()

            # Fallback: pick the latest date found in the document (likely expiration)
            date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"
            all_dates = re.findall(date_pattern, text)

            if all_dates:
                parsed_dates = []
                for d in all_dates:
                    try:
                        parsed_dates.append(datetime.strptime(d, "%d/%m/%Y").date())
                    except ValueError:
                        continue
                
                if parsed_dates:
                    # Return the latest date (most likely to be expiration)
                    return max(parsed_dates)

            raise ErrorExtractingDataException("expiration_date", ValueError("Expiration date not found in PDF"))

        except ErrorExtractingDataException:
            raise
        except Exception as exc:
            raise ErrorExtractingDataException("expiration_date", exc)
