import pytest
from unittest.mock import Mock

from pathlib import Path

from datetime import date
from automacao_certificados.selenium_automations.adapters.extractors import CertificadoMaceioExtractor
from automacao_certificados.selenium_automations.adapters.extractors.exceptions import ErrorExtractingDataException

class TestCertificadoMaceioExtractor:
    def test_if_raises_value_error_if_pdf_path_is_not_a_string_or_path(self):
        """
        Test if the CertificadoMaceioExtractor raises a ValueError if the pdf_path is not a string or Path object.
        """
        with pytest.raises(ValueError) as e:
            CertificadoMaceioExtractor(pdf_path="not_a_string_or_path")
        assert "pdf_path" in str(e.value)

    def test_if_raises_file_not_found_error_if_pdf_path_does_not_exist(self):
        """
        Test if the CertificadoMaceioExtractor raises a FileNotFoundError if the pdf_path does not exist.
        """
        with pytest.raises(FileNotFoundError) as e:
            CertificadoMaceioExtractor(pdf_path=Path("not_a_file.pdf"))
        assert "PDF file not found" in str(e.value)

    def test_if_raises_value_error_if_pdf_path_is_not_a_pdf(self):
        """
        Test if the CertificadoMaceioExtractor raises a ValueError if the pdf_path is not a PDF.
        """
        with pytest.raises(ValueError) as e:
            CertificadoMaceioExtractor(pdf_path=Path("not_a_pdf.txt"))
        assert "File must be a PDF" in str(e.value)

    def test_if_raises_error_extracting_data_exception_if_get_supplier_name_raises_exception(
        self,
        tmp_path: Path,
    ):
        """
        Test if the CertificadoMaceioExtractor raises a ErrorExtractingDataException if the get_supplier_name method raises an exception.
        """
        pdf_path = tmp_path / "certidao_maceio.pdf"
        pdf_path.write_text("Test PDF")

        with pytest.raises(ErrorExtractingDataException) as e:
            CertificadoMaceioExtractor(pdf_path=pdf_path)._get_supplier_name()
        
        assert "supplier_name" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_raises_error_extracting_data_exception_if_get_supplier_cnpj_raises_exception(
        self,
        tmp_path: Path,
    ):
        """
        Test if the CertificadoMaceioExtractor raises a ErrorExtractingDataException if the get_supplier_cnpj method raises an exception.
        """
        pdf_path = tmp_path / "certidao_maceio.pdf"
        pdf_path.write_text("Test PDF")

        with pytest.raises(ErrorExtractingDataException) as e:
            CertificadoMaceioExtractor(pdf_path=pdf_path)._get_supplier_cnpj()
        
        assert "cnpj" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_raises_error_extracting_data_exception_if_get_identifier_raises_exception(
        self,
        tmp_path: Path,
    ):
        """
        Test if the CertificadoMaceioExtractor raises a ErrorExtractingDataException if the get_identifier method raises an exception.
        """
        pdf_path = tmp_path / "certidao_maceio.pdf"
        pdf_path.write_text("Test PDF")

        with pytest.raises(ErrorExtractingDataException) as e:
            CertificadoMaceioExtractor(pdf_path=pdf_path).get_identifier()
        
        assert "identifier" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_document_type_returns_correct_document_type(
        self,
        tmp_path: Path,
    ):
        """
        Test if the CertificadoMaceioExtractor returns the correct document type.
        """
        pdf_path = tmp_path / "certidao_maceio.pdf"
        pdf_path.write_text("Test PDF")

        extractor = CertificadoMaceioExtractor(pdf_path=pdf_path)
        assert extractor.get_document_type() == "CERTIDAO MUNICIPAL MACEIO"

class TestCertificadoMaceioExtractorWithRealPdf:
    def test_if_returns_correct_data_from_real_pdf_1(self):
        path = Path("tests/data/certificados/certificados_maceio/certidao_maceio_1.pdf")

        extractor = CertificadoMaceioExtractor(pdf_path=path)
        assert extractor.get_document_type() == "CERTIDAO MUNICIPAL MACEIO"
        assert extractor.get_identifier() == "0.998.062/25-12"
        assert extractor.get_expiration_date() == date(2026, 2, 1)
        assert extractor.get_supplier().cnpj == "60.604.235/0001-14"

    def test_if_returns_correct_data_from_real_pdf_2(self):
        path = Path("tests/data/certificados/certificados_maceio/certidao_maceio_2.pdf")

        extractor = CertificadoMaceioExtractor(pdf_path=path)
        assert extractor.get_document_type() == "CERTIDAO MUNICIPAL MACEIO"
        assert extractor.get_identifier() == "0.998.126/25-01"
        assert extractor.get_expiration_date() == date(2026, 2, 1)
        assert extractor.get_supplier().cnpj == "22.935.016/0001-29"