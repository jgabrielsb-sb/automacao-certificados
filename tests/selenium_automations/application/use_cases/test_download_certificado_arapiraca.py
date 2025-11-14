from automacao_certificados.selenium_automations.application.use_cases import download_certificado_arapiraca

from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters.selenium.exceptions import *
from automacao_certificados.selenium_automations.application.use_cases.exceptions import *

import pytest

class TestDownloadCertificadoArapiraca:
    def test_download_certificado_arapiraca(self):
        document_extracted, base64_pdf = download_certificado_arapiraca(
            cnpj="21818221000141"
        )
        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)

    def test_download_certificado_arapiraca_2(self):
        document_extracted, base64_pdf = download_certificado_arapiraca(
            cnpj="39549075000161"
        )
        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)

    def test_download_certificado_with_cnpj_with_less_than_14_digits(self):
        with pytest.raises(DownloadCertificadoArapiracaException) as e:
            document_extracted, base64_pdf = download_certificado_arapiraca(
                cnpj="2181000141"
            )
        assert isinstance(e.value.original_exception, IncorrectCNPJException)
        
    def test_download_certificado_with_cnpj_with_more_than_14_digits(self):
        with pytest.raises(DownloadCertificadoArapiracaException) as e:
            document_extracted, base64_pdf = download_certificado_arapiraca(
                cnpj="2181123450001411223"
            )

        assert isinstance(e.value.original_exception, IncorrectCNPJException)
        
    def test_download_certificado_with_invalid_cnpj(self):
        with pytest.raises(DownloadCertificadoArapiracaException) as e:
            document_extracted, base64_pdf = download_certificado_arapiraca(
                cnpj="12345678912345"
            )

        assert isinstance(e.value.original_exception, IncorrectCNPJException)
    