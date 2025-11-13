from automacao_certificados.selenium_automations.application.use_cases import download_certificado_maceio
from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.exceptions import *
from automacao_certificados.selenium_automations.application.use_cases.exceptions import *
from automacao_certificados.selenium_automations.core.models import dto_document

from pathlib import Path

import pytest

class TestDownloadCertificadoMaceio:
    def test_if_raises_download_certidao_estadual_al_exception_if_cnpj_is_not_a_number(self):
        with pytest.raises(DownloadCertificadoMaceioException) as e:
            download_certificado_maceio(
                cnpj="wrong_cnpj",
            )

        assert "must be a number" in str(e.value)

    def test_if_raises_download_certidao_estadual_al_exception_if_cnpj_has_less_than_14_digits(self):
        with pytest.raises(DownloadCertificadoMaceioException) as e:
            download_certificado_maceio(
                cnpj="123",
            )

        assert "cnpj must have 14 digits" in str(e.value)

    def test_sucess_case(self):
        document_extracted, base64_pdf = download_certificado_maceio(
            cnpj="32652832000189",
        )
        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)

    
    
    # def test_sucess_case(self, tmp_path: Path):
    #     document_extracted, base64_pdf = download_certidao_estadual_al(
    #         state_value="AL",
    #         inscricao_value="15401595000164",
    #         img_path_to_save=tmp_path / "certificado.png",
    #     )

    #     assert isinstance(document_extracted, dto_document.DocumentExtracted)
    #     assert isinstance(base64_pdf, str)


        