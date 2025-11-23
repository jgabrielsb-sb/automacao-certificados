import pytest
import base64
from datetime import date

from automacao_certificados.selenium_automations.adapters.extractors.certificado_alagoas_extractor import CertificadoAlagoasExtractor
from automacao_certificados.selenium_automations.core.models import dto_document, dto_supplier
class TestCertificadoAlagoasExtractor:
    @pytest.fixture
    def base64_pdf(self):
        path_to_pdf = "tests/data/certificados/certificados_alagoas/certificado_alagoas_1.pdf"
        with open(path_to_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        return base64_pdf

    def test_extractor_returns_correct_document_type(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_document_type()
        assert document_extracted == "Certidão Negativa Estadual"

    def test_extractor_returns_correct_supplier(
        self,
        base64_pdf: str
    ) -> None:
        supplier = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_supplier()
        assert supplier == dto_supplier.Supplier(
            cnpj="32.652.832/0001-89"
        )

    def test_extractor_returns_correct_expiration_date(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_expiration_date()
        assert document_extracted == date(2026, 1, 16)

    def test_extractor_returns_correct_identifier(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_identifier()
        assert document_extracted == "4DC3-FF14-988E-4361"

    def test_run(self, base64_pdf: str) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).run()

        assert document_extracted == dto_document.DocumentExtracted(
            supplier=dto_supplier.Supplier(
                cnpj="32.652.832/0001-89"
            ),
            document_type="Certidão Negativa Estadual",
            expiration_date=date(2026, 1, 16),
            identifier="4DC3-FF14-988E-4361"
        )

class TestCertificadoAlagoasExtractor2:
    @pytest.fixture
    def base64_pdf(self):
        path_to_pdf = "tests/data/certificados/certificados_alagoas/certificado_alagoas_2.pdf"
        with open(path_to_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        return base64_pdf

    def test_extractor_returns_correct_document_type(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_document_type()
        assert document_extracted == "Certidão Negativa Estadual"

    def test_extractor_returns_correct_expiration_date(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_expiration_date()
        assert document_extracted == date(2026, 1, 16)
    def test_extractor_returns_correct_supplier(
        self,
        base64_pdf: str
    ) -> None:
        supplier = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_supplier()
        assert supplier == dto_supplier.Supplier(
            cnpj="19.322.123/0001-77"
        )
    def test_extractor_returns_correct_identifier(
        self,
        base64_pdf: str
    ) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).get_identifier()
        
        assert document_extracted == "F8F3-C99E-2C49-459D"

    def test_run(self, base64_pdf: str) -> None:
        document_extracted = CertificadoAlagoasExtractor(
            base64_pdf=base64_pdf
        ).run()

        assert document_extracted == dto_document.DocumentExtracted(
            supplier=dto_supplier.Supplier(
                cnpj="19.322.123/0001-77"
            ),
            document_type="Certidão Negativa Estadual",
            expiration_date=date(2026, 1, 16),
            identifier="F8F3-C99E-2C49-459D"
        )
    