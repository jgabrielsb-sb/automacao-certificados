from automacao_certificados.selenium_automations.adapters import DocumentAlagoasDownloader
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters.api_requester.alagoas_api_requester import AlagoasAPIRequester
from automacao_certificados.selenium_automations.adapters.http import HttpxClient

import pytest

class TestDocumentAlagoasDownloader:
    def est_if_raises_download_certidao_estadual_al_exception_if_incorrect_cnpj(self):
        with pytest.raises(ValueError) as e:
            DocumentAlagoasDownloader(
                api_requester=AlagoasAPIRequester(
                    http=HttpxClient()
                )
            ).run(cnpj="wrong_cnpj")

        assert "cnpj must be a number" in str(e.value)

    # def test_if_raises_download_certidao_estadual_al_exception_if_not_basic_cnpj(self):
    #     with pytest.raises(DownloadCertidaoEstadualAlException) as e:
    #         download_certidao_estadual_al(
    #             state_value="AL",
    #             inscricao_value="32652832000189",
    #             img_path_to_save=Path("certificado.png"),
    #         )

    #     assert isinstance(e.value.original_exception, NotBasicCNPJException)

    # 
    
    def test_sucess_case(self):
        document_extracted, base64_pdf = DocumentAlagoasDownloader(
            api_requester=AlagoasAPIRequester(
                http=HttpxClient()
            )
        ).run(cnpj="32652832000189")
        

        assert isinstance(document_extracted, dto_document.DocumentExtracted)
        assert isinstance(base64_pdf, str)


        