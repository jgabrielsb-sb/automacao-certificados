import pytest

from pathlib import Path
import base64

from datetime import date

from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.extractors import *


class TestCertificadoPenedoExtractor:
    def test_if_raises_value_error_if_not_str(self):
        with pytest.raises(ValueError):
            CertificadoPenedoExtractor(base64_pdf=123)

    def test_if_raises_value_error_if_empty_string(self):
        with pytest.raises(ValueError):
            CertificadoPenedoExtractor(base64_pdf="")

    def test_if_raises_value_error_if_invalid_base64_string(self):
        with pytest.raises(ValueError):
            CertificadoPenedoExtractor(base64_pdf="invalid base64 string")

    def test_if_raises_value_error_if_not_valid_pdf_file(self):
        with pytest.raises(ValueError):
            CertificadoPenedoExtractor(base64_pdf=base64.b64encode(b"not a valid pdf file").decode("utf-8"))


class TestCertificadoPenedoExtractorWithRealPdf:
    def test_if_returns_correct_data_from_real_pdf_1(self):
        path = Path("tests/data/certificados/certificados_penedo/certidao_penedo_1.pdf")
        
        with open(path, "rb") as f:
            bytes_data = f.read()
        base64_str = base64.b64encode(bytes_data).decode("utf-8")

        extractor = CertificadoPenedoExtractor(base64_pdf=base64_str)
        assert extractor.get_document_type() == "Certidão Negativa de Débitos Imobiliários"
        assert extractor.get_identifier() == "C55AF87FE5A1253489AA2EBFD9FA240C350D126E"
        assert extractor.get_expiration_date() == date(2026, 3, 29)
        assert extractor.get_supplier().cnpj == "12.243.697/0001-00"
