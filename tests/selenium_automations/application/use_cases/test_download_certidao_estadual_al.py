from automacao_certificados.selenium_automations.application.use_cases import download_certidao_estadual_al
from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.exceptions import *
from automacao_certificados.selenium_automations.application.use_cases.exceptions import *
from automacao_certificados.selenium_automations.core.models import dto_document

from pathlib import Path

import pytest

class TestDownloadCertidaoEstadualAl:
    def est_if_raises_download_certidao_estadual_al_exception_if_incorrect_cnpj(self):
        with pytest.raises(DownloadCertidaoEstadualAlException) as e:
            download_certidao_estadual_al(
                state_value="AL",
                inscricao_value="wrong_cnpj",
                img_path_to_save=Path("certificado.png"),
            )

        assert isinstance(e.value.original_exception, IncorrectCNPJException)

    # def test_if_raises_download_certidao_estadual_al_exception_if_not_basic_cnpj(self):
    #     with pytest.raises(DownloadCertidaoEstadualAlException) as e:
    #         download_certidao_estadual_al(
    #             state_value="AL",
    #             inscricao_value="32652832000189",
    #             img_path_to_save=Path("certificado.png"),
    #         )

    #     assert isinstance(e.value.original_exception, NotBasicCNPJException)

    # 
    
    def test_sucess_case(self, tmp_path: Path):
        document_extracted, base64_pdf = download_certidao_estadual_al(
            state_value="AL",
            inscricao_value="15401595000164",
            img_path_to_save=tmp_path / "certificado.png",
        )

        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)


        