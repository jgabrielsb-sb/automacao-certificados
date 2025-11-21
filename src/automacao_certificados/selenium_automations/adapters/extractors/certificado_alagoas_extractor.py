from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

from datetime import datetime, date
from io import BytesIO
import base64
import re
import pdfplumber


class CertificadoAlagoasExtractor(DocumentExtractorPort):
    """
    Extractor for the Certidão Estadual de Alagoas.
    Accepts ONLY a base64 string representing a PDF.
    
    Based on CertificadoMaceioExtractor; adjust the regex
    patterns below if the Alagoas layout differs.
    """

    def __init__(self, base64_pdf: str):
        """
        Args:
            base64_pdf (str): A BASE64 string that encodes a PDF file.
        """
        print(type(base64_pdf))
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

    # ---------------------------------------------------------------------
    # Internals
    # ---------------------------------------------------------------------

    def _load_pdf_text(self) -> str:
        """
        Decode PDF bytes → extract text from ALL pages.
        """
        if self._pdf_text is not None:
            return self._pdf_text

        with pdfplumber.open(BytesIO(self._pdf_bytes)) as pdf:
            self._pdf_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        return self._pdf_text

    # ---------------------------------------------------------------------
    # Extraction Methods
    # ---------------------------------------------------------------------

    def _get_supplier_cnpj(self) -> str:
        """
        Extract the CNPJ from the PDF text.
        """
        try:
            text = self._load_pdf_text()

            cnpj_pattern = r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b"
            match = re.search(cnpj_pattern, text)

            return match.group(1) if match else None

        except Exception as exc:
            raise ErrorExtractingDataException("cnpj", exc)

    def _get_supplier_name(self) -> str:
        """
        Extract the supplier name from the PDF text.
        """
        try:
            text = self._load_pdf_text()

            patterns = [
                r"(?:Razão Social|Razão\s+Social|Nome\s+Empresarial)[:\s]*([^\n]+)",
                r"(?:Nome\s+da\s+Empresa|Empresa)[:\s]*([^\n]+)",
                r"CNPJ[:\s]*\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}[^\n]*\n([^\n]+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    name = re.sub(r"\s+", " ", name)
                    if name:
                        return name
        except Exception as exc:
            raise ErrorExtractingDataException("supplier_name", exc)

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
        return "Certidão Negativa Estadual"

    def get_identifier(self) -> str:
        """
        Extract the certificate identifier/number.
        For Alagoas certificates, this is typically a hexadecimal code like "4DC3-FF14-988E-4361".
        """
        try:
            text = self._load_pdf_text()

            # Pattern 1: Look for "Código de controle" followed by the identifier
            # This is the primary pattern for Alagoas certificates
            # Handles "Código de controle da certidão: 4DC3-FF14-988E-4361"
            pattern1 = r"Código\s+de\s+controle[^:]*:\s*([A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4})"
            match = re.search(pattern1, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

            # Pattern 2: Look for hexadecimal code format (4 groups of 4 hex chars separated by dashes)
            # This is the format used in Alagoas certificates: "4DC3-FF14-988E-4361"
            pattern2 = r"\b([A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4})\b"
            match = re.search(pattern2, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

            # Pattern 3: Try protocol pattern (common in Brazilian certificates)
            protocol_pattern = r"\b(\d+\.\d+\.\d+/\d{2}-\d{2})\b"
            match = re.search(protocol_pattern, text)
            if match:
                return match.group(1)

            # Pattern 4: Try other common patterns
            patterns = [
                r"(?:Número|Nº|Numero|Certificado)[\s:]*([A-Z0-9\./\-]+)",
                r"(?:Protocolo|Protocolo\s+Número)[\s:]*([A-Z0-9\./\-]+)",
                r"(?:Código|Código\s+da\s+Certidão)[\s:]*([A-Z0-9\./\-]+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    return match.group(1).strip()

        except Exception as exc:
            raise ErrorExtractingDataException("identifier", exc)

    def get_expiration_date(self) -> date:
        """
        Extract the expiration date of the certificate.
        """
        try:
            text = self._load_pdf_text()

            patterns = [
                r"(?:Válida\s+até|Válido\s+até|Validade|Vencimento)[\s:]*(\d{2}/\d{2}/\d{4})",
                r"(?:Expira\s+em|Expiração)[\s:]*(\d{2}/\d{2}/\d{4})",
                r"(\d{2}/\d{2}/\d{4})\s+(?:a|até)\s+(\d{2}/\d{2}/\d{4})",
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

            # Fallback: pick the latest date found in the document
            date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"
            all_dates = re.findall(date_pattern, text)

            if all_dates:
                parsed = [
                    datetime.strptime(d, "%d/%m/%Y").date()
                    for d in all_dates
                ]
                return max(parsed)

        except Exception as exc:
            raise ErrorExtractingDataException("expiration_date", exc)

