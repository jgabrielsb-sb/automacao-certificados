from pathlib import Path

from datetime import date

import base64

import pytest

from selenium.webdriver.support.expected_conditions import url_changes

from automacao_certificados.selenium_automations.adapters.extractors.certificado_federal_extractor import CertificadoFederalExtractor
from automacao_certificados.selenium_automations.core.models import Supplier

class TestCertificadoFederalPraticalCase1:
    file_path = 'tests/data/certificados/certificados_federal/CNPJ14868712000131.pdf'

    @pytest.fixture
    def mock_extractor(self):
        with open(self.file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        
        return CertificadoFederalExtractor(base64_pdf)


    def test_get_expiration_date(self, mock_extractor):
        expiration_date = mock_extractor.get_expiration_date()

        assert expiration_date == date(2026, 5, 30)

    def test_supplier_name(self, mock_extractor):
        supplier_name = mock_extractor._get_supplier_name()

        assert supplier_name == "AKAD SEGUROS S.A"

    def test_get_supplier_cnpj(self, mock_extractor):
        supplier_cnpj = mock_extractor._get_supplier_cnpj()

        assert supplier_cnpj == "14.868.712/0001-31"

    def test_get_supplier(self, mock_extractor):
        supplier = mock_extractor.get_supplier()

        assert supplier == Supplier(
            cnpj="14.868.712/0001-31"
        )

    def test_get_document_type(self, mock_extractor):
        document_type = mock_extractor.get_document_type()

        assert document_type == 'Certidão Negativa Federal'

    def test_get_identifier(self, mock_extractor):
        identifier = mock_extractor.get_identifier()

        assert identifier == "CE62.389C.D8B7.F57D"

class TestCertificadoFederalPraticalCase2:
    file_path = 'tests/data/certificados/certificados_federal/Certidao-45873047000106.pdf'

    @pytest.fixture
    def mock_extractor(self):
        with open(self.file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        
        return CertificadoFederalExtractor(base64_pdf)


    def test_get_expiration_date(self, mock_extractor):
        expiration_date = mock_extractor.get_expiration_date()

        assert expiration_date == date(2025, 8, 20)

    def test_supplier_name(self, mock_extractor):
        supplier_name = mock_extractor._get_supplier_name()

        assert supplier_name == "L F L VASCONCELLOS LTDA"

    def test_get_supplier_cnpj(self, mock_extractor):
        supplier_cnpj = mock_extractor._get_supplier_cnpj()

        assert supplier_cnpj == "45.873.047/0001-06"

    def test_get_supplier(self, mock_extractor):
        supplier = mock_extractor.get_supplier()

        assert supplier == Supplier(
            cnpj="45.873.047/0001-06"
        )

    def test_get_document_type(self, mock_extractor):
        document_type = mock_extractor.get_document_type()

        assert document_type == 'Certidão Negativa Federal'

    def test_get_identifier(self, mock_extractor):
        identifier = mock_extractor.get_identifier()

        assert identifier == "88BD.E858.CE6D.5144"

class TestCertificadoFederalPraticalCase3:
    file_path = 'tests/data/certificados/certificados_federal/Certidao-Federal-04722126000120.pdf'

    @pytest.fixture
    def mock_extractor(self):
        with open(self.file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        
        return CertificadoFederalExtractor(base64_pdf)

    def test_get_expiration_date(self, mock_extractor):
        expiration_date = mock_extractor.get_expiration_date()

        assert expiration_date == date(2026, 5, 31)

    def test_supplier_name(self, mock_extractor):
        supplier_name = mock_extractor._get_supplier_name()

        assert supplier_name == "ELEMAC ELEVADORES LTDA"

    def test_get_supplier_cnpj(self, mock_extractor):
        supplier_cnpj = mock_extractor._get_supplier_cnpj()

        assert supplier_cnpj == "04.722.126/0001-20"

    def test_get_supplier(self, mock_extractor):
        supplier = mock_extractor.get_supplier()

        assert supplier == Supplier(
            cnpj="04.722.126/0001-20"
        )

    def test_get_document_type(self, mock_extractor):
        document_type = mock_extractor.get_document_type()

        assert document_type == 'Certidão Negativa Federal'

    def test_get_identifier(self, mock_extractor):
        identifier = mock_extractor.get_identifier()

        assert identifier == "18A8.FC3F.99B3.6D28"