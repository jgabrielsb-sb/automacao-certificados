import pytest


from pathlib import Path
import base64

from datetime import date

from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.extractors import *

class TestCertificadoMaceioExtractor:
    def test_if_raises_value_error_if_not_str(self):
        with pytest.raises(ValueError):
            CertificadoMaceioExtractor(base64_pdf=123)


    def test_if_raises_value_error_if_empty_string(self):
        with pytest.raises(ValueError):
            CertificadoMaceioExtractor(base64_pdf="")

    def test_if_raises_value_error_if_invalid_base64_string(self):
        with pytest.raises(ValueError):
            CertificadoMaceioExtractor(base64_pdf="invalid base64 string")

    def test_if_raises_value_error_if_not_valid_pdf_file(self):
        with pytest.raises(ValueError):
            CertificadoMaceioExtractor(base64_pdf="not a valid pdf file")

class TestCertificadoMaceioExtractorWithRealPdf:
    def test_if_returns_correct_data_from_real_pdf_1(self):
        path = Path("tests/data/certificados/certificados_maceio/certidao_maceio_1.pdf")
        
        bytes = open(path, "rb")
        base64_str = base64.b64encode(bytes.read()).decode("utf-8")

        extractor = CertificadoMaceioExtractor(base64_pdf=base64_str)
        assert extractor.get_document_type() == "Certidão Negativa Municipal"
        assert extractor.get_identifier() == "0.998.062/25-12"
        assert extractor.get_expiration_date() == date(2026, 2, 1)
        assert extractor.get_supplier().cnpj == "60.604.235/0001-14"

    def test_if_returns_correct_data_from_real_pdf_2(self):
        path = Path("tests/data/certificados/certificados_maceio/certidao_maceio_2.pdf")
        
        bytes = open(path, "rb")
        base64_str = base64.b64encode(bytes.read()).decode("utf-8")
        
        extractor = CertificadoMaceioExtractor(base64_pdf=base64_str)
        assert extractor.get_document_type() == "Certidão Negativa Municipal"
        assert extractor.get_identifier() == "0.998.126/25-01"
        assert extractor.get_expiration_date() == date(2026, 2, 1)
        assert extractor.get_supplier().cnpj == "22.935.016/0001-29"