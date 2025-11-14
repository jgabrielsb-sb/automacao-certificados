import base64
from datetime import date

from automacao_certificados.selenium_automations.adapters.extractors import CertidaoArapiracaExtractor
from automacao_certificados.selenium_automations.core.models import dto_document

import pytest

class TestCertificadoArapiraca1Extractor:
    @pytest.fixture
    def html_content(self):
        path_to_pdf = "tests/data/certificados/certificados_arapiraca/certificado_arapiraca_1.html"
        with open(path_to_pdf, "r") as file:
            html_content = file.read()
        return html_content

    def test_extractor_returns_correct_document_type(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_document_type()
        assert document_extracted == "CERTIDAO MUNICIPAL ARAPIRACA"

    def test_extractor_returns_correct_expiration_date(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_expiration_date()
        assert document_extracted == date(2026, 1, 12)

    def test_extractor_returns_correct_identifier(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_identifier()
        assert document_extracted == "491441535"

class TestCertificadoArapiraca2Extractor:
    @pytest.fixture
    def html_content(self):
        path_to_pdf = "tests/data/certificados/certificados_arapiraca/certificado_arapiraca_2.html"
        with open(path_to_pdf, "r") as file:
            html_content = file.read()
        return html_content

    def test_extractor_returns_correct_document_type(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_document_type()
        assert document_extracted == "CERTIDAO MUNICIPAL ARAPIRACA"

    def test_extractor_returns_correct_expiration_date(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_expiration_date()
        print(document_extracted)
        assert document_extracted == date(2025, 12, 11)

    def test_extractor_returns_correct_identifier(
        self,
        html_content: str
    ) -> None:
        document_extracted = CertidaoArapiracaExtractor(
            html_content=html_content
        ).get_identifier()
        assert document_extracted == "491391609"

# 