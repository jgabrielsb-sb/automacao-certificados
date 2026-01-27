from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.adapters.http import HttpxClient

import pytest
import respx
from httpx import Response
from pathlib import Path
import base64

BASE_URL = "https://contribuinte.sefaz.al.gov.br"

class TestAlagoasAPIRequester:
    @respx.mock
    def test_sucess_response(self):
        file_path = "tests/data/certificados/certificados_maceio/certidao_maceio_1.pdf"
        
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        file_content_b64 = base64.b64encode(file_content).decode("utf-8")
        
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(200, json={
                'nomeRelatorio': 'certidao-negativa-debito - 32652832000189 em 17-11-2025_14-27-33.pdf', 
                'conteudo': file_content_b64}
            )
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        response = api_requester.get_certificado(cnpj="32652832000189")
        
        assert route.called
        assert response == file_content_b64

    @respx.mock
    def test_200_response_with_no_content(self):
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(200, json={
                'nomeRelatorio': 'certidao-negativa-debito - 32652832000189 em 17-11-2025_14-27-33.pdf', 
            })
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        with pytest.raises(UnexpectedError) as e:
            api_requester.get_certificado(cnpj="32652832000189")

        assert route.called
        assert e.value.message == "Unexpected error. The API Response does not have 'conteudo' key. API Response: {'nomeRelatorio': 'certidao-negativa-debito - 32652832000189 em 17-11-2025_14-27-33.pdf'}"

    @respx.mock
    def test_200_response_with_invalid_cnpj(self):
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(500, json={
                'message': 'error.documento', 
                'description': 'CNPJ inválido ou não informado.', 
                'status': 1, 
                'fieldErrors': None
            })
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        with pytest.raises(InvalidCNPJException) as e:
            api_requester.get_certificado(cnpj="32652732000189")

        assert route.called
        assert e.value.message == "CNPJ is invalid or does not exist: 32652732000189. API Response: {'message': 'error.documento', 'description': 'CNPJ inválido ou não informado.', 'status': 1, 'fieldErrors': None}"

    @respx.mock
    def test_200_response_with_unexpected_error(self):
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(400, json={
                'message': 'unexpected error'
            })
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        with pytest.raises(UnexpectedError) as e:
            api_requester.get_certificado(cnpj="32652732000189")

        assert route.called
        assert e.value.message == "Unexpected error: API Response: {'message': 'unexpected error'}"

    @respx.mock
    def test_500_response_with_could_not_generate_pdf(self):
        json_response = {
            'message': 'error.validation', 
            'description': 'Não foi possível emitir a Certidão Positiva com Efeito Negativo para esse CNPJ conforme Art. 258 do Decreto 25.370 de 19 de março de 2013!', 
            'status': 0, 
            'fieldErrors': None
        }
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(
                500, 
                json=json_response
            )
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        with pytest.raises(CouldNotGeneratePDF) as e:
            api_requester.get_certificado(cnpj="32652732000189")

        assert route.called
        assert e.value.message == f"Could not generate PDF caused by CNPJ issues: API Response: {json_response}"

    @respx.mock
    def test_500_response_with_unexpected_error(self):
        json_response = {
            'message': 'unexpected error'
        }
        route = respx.post(f"{BASE_URL}/certidao/sfz-certidao-api/api/public/emitirCertidao").mock(
            return_value=Response(500, json=json_response)
        )

        api_requester = AlagoasAPIRequester(
            base_url=BASE_URL,
            http=HttpxClient()
        )

        with pytest.raises(UnexpectedError) as e:
            api_requester.get_certificado(cnpj="32652732000189")

        assert route.called
        assert e.value.message == f"Unexpected error. API Response: {json_response}"

    