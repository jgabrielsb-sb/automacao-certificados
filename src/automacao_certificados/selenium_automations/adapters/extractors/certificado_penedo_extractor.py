import base64
import re
from datetime import datetime, date
from io import BytesIO

import pdfplumber

from automacao_certificados.selenium_automations.core.interfaces import DocumentExtractorPort
from automacao_certificados.selenium_automations.core.models import dto_supplier
from automacao_certificados.selenium_automations.core.exceptions import ErrorExtractingDataException


class CertificadoPenedoExtractor(DocumentExtractorPort):
    """
    Extractor for the Certidão Negativa de Débitos Imobiliários from Município de Penedo.
    Accepts ONLY a base64 string representing a PDF.
    """

    def __init__(self, base64_pdf: str):
        if not isinstance(base64_pdf, str):
            raise ValueError("base64_pdf must be a string")
        if not base64_pdf.strip():
            raise ValueError("base64_pdf string is empty")

        try:
            pdf_bytes = base64.b64decode(base64_pdf.encode("ascii"))
        except Exception as exc:
            raise ValueError("Invalid base64 PDF string") from exc

        if not pdf_bytes.startswith(b"%PDF"):
            raise ValueError("Decoded data is not a valid PDF file")

        self._pdf_bytes = pdf_bytes
        self._pdf_text: str | None = None

    def _load_pdf_text(self) -> str:
        if self._pdf_text is not None:
            return self._pdf_text

        with pdfplumber.open(BytesIO(self._pdf_bytes)) as pdf:
            self._pdf_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        return self._pdf_text

    def _get_supplier_cnpj(self) -> str:
        try:
            text = self._load_pdf_text()
            # Example: 12.243.697/0001-00
            match = re.search(r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b", text)
            if not match:
                raise ValueError("CNPJ not found in PDF text")
            return match.group(1)
        except Exception as exc:
            raise ErrorExtractingDataException("cnpj", exc)

    def get_supplier(self) -> dto_supplier.Supplier:
        return dto_supplier.Supplier(cnpj=self._get_supplier_cnpj())

    def get_document_type(self) -> str:
        return "Certidão Negativa"

    def get_identifier(self) -> str:
        """
        In Penedo PDFs this is the 'Código de Verificação'.
        Example: C55AF87FE5A1253489AA2EBFD9FA240C350D126E
        """
        try:
            text = self._load_pdf_text()

            # Primary: labeled code
            m = re.search(
                r"C[oó]digo\s+de\s+Verifica[cç][aã]o:\s*([A-F0-9]{16,})",
                text,
                re.IGNORECASE | re.MULTILINE,
            )
            if m:
                return m.group(1).strip()

            # Fallback: long hex token present anywhere
            m = re.search(r"\b([A-F0-9]{32,})\b", text, re.IGNORECASE)
            if m:
                return m.group(1).strip()

            raise ValueError("identifier not found in PDF text")
        except Exception as exc:
            raise ErrorExtractingDataException("identifier", exc)

    def get_expiration_date(self) -> date:
        """
        In Penedo PDFs this is the 'Validade' field.
        Example: 29/03/2026
        """
        try:
            text = self._load_pdf_text()

            m = re.search(
                r"Validade\s*:\s*(\d{2}/\d{2}/\d{4})",
                text,
                re.IGNORECASE | re.MULTILINE,
            )
            if m:
                return datetime.strptime(m.group(1), "%d/%m/%Y").date()

            # Fallback: pick latest date in document (usually validity is the latest)
            all_dates = re.findall(r"\b(\d{2}/\d{2}/\d{4})\b", text)
            if all_dates:
                parsed = [datetime.strptime(d, "%d/%m/%Y").date() for d in all_dates]
                return max(parsed)

            raise ValueError("expiration date not found in PDF text")
        except Exception as exc:
            raise ErrorExtractingDataException("expiration_date", exc)

