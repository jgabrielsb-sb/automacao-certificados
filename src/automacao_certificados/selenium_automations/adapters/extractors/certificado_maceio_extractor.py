from automacao_certificados.selenium_automations.core.interfaces import*
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

from datetime import datetime, date
from io import BytesIO
import base64
import re
import pdfplumber


class CertificadoMaceioExtractor(DocumentExtractorPort):
    """
    Extractor for the Certificado Municipal Maceió.
    Accepts ONLY a base64 string representing a PDF.
    """

    def __init__(self, base64_pdf: str):
        """
        The certificado maceio extractor is an implementation of the document extractor port 
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

    # ---------------------------------------------------------------------
    # Internals
    # ---------------------------------------------------------------------

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

    # ---------------------------------------------------------------------
    # Extraction Methods
    # ---------------------------------------------------------------------

    def _get_supplier_cnpj(self) -> str:
        """
        Extract the CNPJ from the PDF text.

        :return: The cnpj.
        :rtype: str
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

        :return: The supplier name.
        :rtype: str
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

        :return: The supplier DTO.
        :rtype: dto_supplier.Supplier
        """
        return dto_supplier.Supplier(
            cnpj=self._get_supplier_cnpj(),
        )

    def get_document_type(self) -> str:
        """
        Returns the document type.

        :return: The document type.
        :rtype: str
        """
        return "Certidão Negativa Municipal"

    def get_identifier(self) -> str:
        """
        Extract the document identifier/number.

        :return: The document identifier.
        :rtype: str
        """
        try:
            text = self._load_pdf_text()

            protocol_pattern = r"\b(\d+\.\d+\.\d+/\d{2}-\d{2})\b"
            match = re.search(protocol_pattern, text)
            if match:
                return match.group(1)

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

        :return: The expiration date.
        :rtype: date
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
                        expiration_str = match.group(2)
                    else:
                        expiration_str = match.group(1)

                    return datetime.strptime(expiration_str, "%d/%m/%Y").date()

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
