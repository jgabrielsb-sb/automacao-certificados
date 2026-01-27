from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester, PPEAPIRequester
from unittest.mock import MagicMock

import pytest

class TestDocumentAlagoasDownloader:
    def test_if_raises_download_certidao_estadual_al_exception_if_incorrect_cnpj(self):
        with pytest.raises(ValueError) as e:
            DocumentAlagoasDownloader(
                api_requester=AlagoasAPIRequester(
                    http=HttpxClient()
                ),
                ppe_api_requester=MagicMock(spec=PPEAPIRequester)
            ).run(input=DocumentDownloaderInput(cnpj="wrong_cnpj"))

        assert "cnpj must be a number" in str(e.value)

    @pytest.mark.selenium_workflow_tests
    def test_sucess_case(self):
        output = DocumentAlagoasDownloader(
            api_requester=AlagoasAPIRequester(
                http=HttpxClient()
            ),
            ppe_api_requester=MagicMock(spec=PPEAPIRequester)
        ).run(input=DocumentDownloaderInput(cnpj="32652832000189"))
        
        
        assert isinstance(output.document_extracted, dto_document.DocumentExtracted)
        assert isinstance(output.base64_pdf, str)

    @pytest.mark.selenium_workflow_tests
    def test_if_raises_sucesso_com_ressalvas_exception_if_cnpj_has_ressalvas(self):
        alagoas_api_requester = MagicMock(spec=AlagoasAPIRequester)
        alagoas_api_requester.get_certificado.side_effect = SucessoComRessalvasException(
            message='test'
        )

        ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        ppe_api_requester.block_certificate.return_value = {
            'message': 'test'
        }
             
        
        with pytest.raises(DocumentDownloaderException) as e:
            DocumentAlagoasDownloader(
                api_requester=alagoas_api_requester,
                ppe_api_requester=ppe_api_requester
            ).run(input=DocumentDownloaderInput(cnpj="32652732000189"))
        
        

class TestBlockOnPPE:
    def test_if_returns_correct_message_when_block_on_ppe_is_sucess(self):
        ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        ppe_api_requester.block_certificate.return_value = {
            'message': 'test'
        }

        expected_message = "OBS: a request to block the search for the certificate was made successfully. The response was: {'message': 'test'}"
        result = DocumentAlagoasDownloader(
            api_requester=MagicMock(spec=AlagoasAPIRequester),
            ppe_api_requester=ppe_api_requester
        )._block_on_ppe(cnpj="32652732000189")
        assert result == expected_message

    def test_if_returns_correct_message_when_block_on_ppe_is_error(self):
        ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        ppe_api_requester.block_certificate.side_effect = APIRequesterException('test')

        expected_message = "OBS: the request to block the search for the certificate got an error: test"
        result = DocumentAlagoasDownloader(
            api_requester=MagicMock(spec=AlagoasAPIRequester),
            ppe_api_requester=ppe_api_requester
        )._block_on_ppe(cnpj="32652732000189")
        assert result == expected_message

class TestGetBase64OrRaiseRessalvas:
    def test_if_returns_correct_base64_when_get_base64_or_raise_ressalvas_is_sucess(self):
        api_requester = MagicMock(spec=AlagoasAPIRequester)
        api_requester.get_certificado.return_value = 'test'

        expected_base64 = 'test'
        result = DocumentAlagoasDownloader(
            api_requester=api_requester,
            ppe_api_requester=MagicMock(spec=PPEAPIRequester)
        )._get_base64_or_raise_ressalvas(cnpj="32652732000189")
        assert result == expected_base64

    def test_if_raises_sucess_with_ressalvas_if_get_certificado_raises_sucess_with_ressalvas_exception_and_block_on_ppe_sucess(self):
        api_requester = MagicMock(spec=AlagoasAPIRequester)
        api_requester.get_certificado.side_effect = SucessoComRessalvasException('test')

        ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        ppe_api_requester.block_certificate.return_value = {
            'message': 'test'
        }

        expected_message = "test. OBS: a request to block the search for the certificate was made successfully. The response was: {'message': 'test'}"
        with pytest.raises(SucessoComRessalvasException) as e:
            DocumentAlagoasDownloader(
                api_requester=api_requester,
                ppe_api_requester=ppe_api_requester
            )._get_base64_or_raise_ressalvas(cnpj="32652732000189")

        assert str(e.value) == expected_message

    def test_if_raises_sucess_with_ressalvas_if_get_certificado_raises_sucess_with_ressalvas_exception_and_block_on_ppe_error(self):
        api_requester = MagicMock(spec=AlagoasAPIRequester)
        api_requester.get_certificado.side_effect = SucessoComRessalvasException('test')

        ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        ppe_api_requester.block_certificate.side_effect = APIRequesterException('test')

        expected_message = "test. OBS: the request to block the search for the certificate got an error: test"
        with pytest.raises(SucessoComRessalvasException) as e:
            DocumentAlagoasDownloader(
                api_requester=api_requester,
                ppe_api_requester=ppe_api_requester
            )._get_base64_or_raise_ressalvas(cnpj="32652732000189")

        assert str(e.value) == expected_message