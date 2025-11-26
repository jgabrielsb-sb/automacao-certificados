from automacao_certificados.selenium_automations.utils.utils import *

import pytest

class TestFormatCNPJ:
    def test_if_raises_value_error_if_not_str(self):
        with pytest.raises(ValueError) as e:
            format_cnpj(123)

        assert "cnpj must be a string" in str(e.value)

    def test_if_raises_value_error_if_not_valid_cnpj(self):
        with pytest.raises(ValueError) as e:
            format_cnpj("123456781234")

        assert "cnpj must have 14 digits" in str(e.value)

    def test_if_raises_value_error_if_not_number(self):
        with pytest.raises(ValueError) as e:
            format_cnpj("12345678901234a")

        assert "cnpj must be a number" in str(e.value)

    def test_if_returns_formatted_cnpj_if_valid(self):
        assert format_cnpj("12345678901234") == "12.345.678/9012-34"

class TestValidateDocumentFile:
    def test_if_raises_value_error_if_not_str(self):
        with pytest.raises(ValueError):
            validate_document_file(123)

    def test_if_raises_value_error_if_invalid_base64_string(self):
        with pytest.raises(ValueError):
            validate_document_file("invalid base64 string")

    def test_if_raises_value_error_if_not_valid_pdf_file(self):
        with pytest.raises(ValueError):
            validate_document_file("invalid pdf file")
    
    def test_if_returns_none_if_valid_pdf_file(self):
        with open("tests/data/certificados/certificados_maceio/certidao_maceio_1.pdf", "rb") as f:
            valid_pdf_b64 = base64.b64encode(f.read()).decode("utf-8")

        assert validate_document_file(valid_pdf_b64) is None