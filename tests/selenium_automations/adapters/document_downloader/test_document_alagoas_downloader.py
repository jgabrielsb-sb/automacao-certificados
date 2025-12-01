from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester

import pytest

class TestDocumentAlagoasDownloader:
    def test_if_raises_download_certidao_estadual_al_exception_if_incorrect_cnpj(self):
        with pytest.raises(ValueError) as e:
            DocumentAlagoasDownloader(
                api_requester=AlagoasAPIRequester(
                    http=HttpxClient()
                )
            ).run(input=DocumentDownloaderInput(cnpj="wrong_cnpj"))

        assert "cnpj must be a number" in str(e.value)

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self):
        output = DocumentAlagoasDownloader(
            api_requester=AlagoasAPIRequester(
                http=HttpxClient()
            )
        ).run(input=DocumentDownloaderInput(cnpj="32652832000189"))
        
        
        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)


        