
from httpx import Response
import respx

import pytest

from automacao_certificados.selenium_automations.adapters.http.httpx_client import HttpxClient
from automacao_certificados.selenium_automations.core.exceptions.adapters.api_requester_exceptions import (
    CouldNotGeneratePDF,
    SucessoComRessalvasException, 
    UnexpectedError, 
    DocumentoEntidadeNaoEncontradaException
)
from automacao_certificados.selenium_automations.core.interfaces.http_client import HttpClient
from automacao_certificados.selenium_automations.infra.api_requester.direct_data_api_requester import DirectDataAPIRequester

SUCESS_JSON_RESPONSE = {
  "metaDados": {
    "consultaNome": "CCD - Certidão Conjunta de Débitos - Pessoa Jurídica",
    "consultaUid": "direct-b15fab09-24a9-45d2-8c15-ace507cf38b8",
    "chave": "CNPJ=14868712000131;",
    "usuario": "João Gabriel Sampaio de Barros",
    "mensagem": "Sucesso",
    "ip": "201.17.208.230",
    "resultadoId": 1,
    "resultado": "Sucesso",
    "apiVersao": "v3",
    "enviarCallback": False,
    "gerarComprovante": True,
    "urlComprovante": "https://apiv3.directd.com.br/api/Historico?ConsultaUid=direct-b15fab09-24a9-45d2-8c15-ace507cf38b8&Extensao=pdf",
    "assincrono": False,
    "data": "02/12/2025 15:40:27",
    "tempoExecucaoMs": 554
  },
  "retorno": {
    "titulo": "CERTIDÃO POSITIVA COM EFEITOS DE NEGATIVA DE DÉBITOS RELATIVOS AOS TRIBUTOS FEDERAIS E À DÍVIDA ATIVA DA UNIÃO",
    "cnpj": "14.868.712/0001-31",
    "nome": "AKAD SEGUROS S.A.",
    "portaria": "Portaria Conjunta RFB/PGFN no 1.751, de 2/10/2014.",
    "emitidaAs": "01/12/2025 15:11:44",
    "validaAte": "30/05/2026 00:00:00",
    "status": "CONSTA",
    "possuiDividas": True,
    "listaDividas": [
      "1. constam débitos administrados pela Secretaria da Receita Federal do Brasil (RFB) com exigibilidade suspensa nos termos do art. 151 da Lei no 5.172, de 25 de outubro de 1966 - Código Tributário Nacional (CTN), ou objeto de decisão judicial que determina sua desconsideração para fins de certificação da regularidade fiscal, ou ainda não vencidos",
      "2. não constam inscrições em Dívida Ativa da União (DAU) na Procuradoria-Geral da Fazenda Nacional (PGFN)."
    ],
    "codigoControleCertidao": "CE62.389C.D8B7.F57D"
  }
}

SUCESS_COM_RESALVAS_JSON_RESPONSE = {
  "metaDados": {
    "consultaNome": "CCD - Certidão Conjunta de Débitos - Pessoa Jurídica",
    "consultaUid": "direct-5f97c62f-a1d7-45ab-be61-42ee283305f3",
    "chave": "CNPJ=17086031000100;",
    "usuario": "João Gabriel Sampaio de Barros",
    "mensagem": "Sucesso Com Ressalvas. As informações disponíveis na Receita Federal e na Procuradoria-Geral da Fazenda Nacional sobre o contribuinte são insuficientes para emitir a certidão pela Internet",
    "ip": "201.17.208.230",
    "resultadoId": 2,
    "resultado": "Sucesso Com Ressalvas",
    "apiVersao": "v3",
    "enviarCallback": False,
    "gerarComprovante": True,
    "urlComprovante": None,
    "assincrono": False,
    "data": "02/12/2025 15:40:53",
    "tempoExecucaoMs": 9736
  },
  "retorno": {
    "titulo": None,
    "cnpj": "17.086.031/0001-00",
    "nome": "ATITUDE SERVICOS DE LIMPEZA LTDA",
    "portaria": None,
    "emitidaAs": None,
    "validaAte": None,
    "status": "As informações disponíveis na Receita Federal e na Procuradoria-Geral da Fazenda Nacional sobre o contribuinte são insuficientes para emitir a certidão pela Internet.",
    "possuiDividas": None,
    "listaDividas": [],
    "codigoControleCertidao": None
  }
}

CERTIDAO_DEVE_SER_ENVIADA_PARA_A_MATRIZ_RESPONSE =  {
  "metaDados": {
    "consultaNome": "CCD - Certidão Conjunta de Débitos - Pessoa Jurídica",
    "consultaUid": "direct-5f97c62f-a1d7-45ab-be61-42ee283305f3",
    "chave": "CNPJ=17086031000100;",
    "usuario": "João Gabriel Sampaio de Barros",
    "mensagem": "Documento Entidade Não Encontrada.A certidão deve ser emitida para a matriz do contribuinte consultado",
    "ip": "201.17.208.230",
    "resultadoId": 2,
    "resultado": "Sucesso Com Ressalvas",
    "apiVersao": "v3",
    "enviarCallback": False,
    "gerarComprovante": True,
    "urlComprovante": None,
    "assincrono": False,
    "data": "02/12/2025 15:40:53",
    "tempoExecucaoMs": 9736
  },
  "retorno": {
    "titulo": None,
    "cnpj": "17.086.031/0001-00",
    "nome": "ATITUDE SERVICOS DE LIMPEZA LTDA",
    "portaria": None,
    "emitidaAs": None,
    "validaAte": None,
    "status": "As informações disponíveis na Receita Federal e na Procuradoria-Geral da Fazenda Nacional sobre o contribuinte são insuficientes para emitir a certidão pela Internet.",
    "possuiDividas": None,
    "listaDividas": [],
    "codigoControleCertidao": None
  }
}

class TestDirectDataAPIRequester:

    @pytest.fixture 
    def mock_direct_data_api_requester(self):
        return DirectDataAPIRequester(
            http=HttpxClient(),
            token="test_token",
            base_url="http://test.com"
        )
    
    @respx.mock
    def test_sucess_get_certificado_url(
        self,
        mock_direct_data_api_requester
    ):
        cnpj = "12345678912345"
        route = respx.get(
            url=f"{mock_direct_data_api_requester.base_url}/api/CertidaoConjuntaDebitosPessoaJuridica"
        ).mock(
            return_value=Response(200, json=SUCESS_JSON_RESPONSE)
        )
        
        certificado_url = mock_direct_data_api_requester.get_certificado_url(cnpj)
        
        assert certificado_url == 'https://apiv3.directd.com.br/api/Historico?ConsultaUid=direct-b15fab09-24a9-45d2-8c15-ace507cf38b8&Extensao=pdf'
        
        
    @respx.mock
    def test_sucess_com_ressalvas_get_certificado_url(
        self,
        mock_direct_data_api_requester
    ):
        cnpj = "12345678912345"
        url = f"{mock_direct_data_api_requester.base_url}/api/CertidaoConjuntaDebitosPessoaJuridica"
        
        route = respx.get(
            url=url
        ).mock(
            return_value=Response(status_code=200, json=SUCESS_COM_RESALVAS_JSON_RESPONSE),
        )

        with pytest.raises(SucessoComRessalvasException) as e:
            mock_direct_data_api_requester.get_certificado_url(cnpj)

        sucesso_com_ressalvas_message = "Sucesso Com Ressalvas. As informações disponíveis na Receita Federal e na Procuradoria-Geral da Fazenda Nacional sobre o contribuinte são insuficientes para emitir a certidão pela Internet"
        
        assert url in str(e.value)
        assert sucesso_com_ressalvas_message in str(e.value)

    @respx.mock
    def test_documento_entidade_nao_encontrada_get_certificado_url(
        self,
        mock_direct_data_api_requester
    ):
        cnpj = "12345678912345"
        url = f"{mock_direct_data_api_requester.base_url}/api/CertidaoConjuntaDebitosPessoaJuridica"
        route = respx.get(url=url).mock(
            return_value=Response(status_code=200, json=CERTIDAO_DEVE_SER_ENVIADA_PARA_A_MATRIZ_RESPONSE),
        )

        with pytest.raises(DocumentoEntidadeNaoEncontradaException) as e:
            mock_direct_data_api_requester.get_certificado_url(cnpj)

        assert url in str(e.value)
        assert "Documento Entidade Não Encontrada" in str(e.value)

    @respx.mock
    def test_unexpected_response(
        self,
        mock_direct_data_api_requester
    ):
        cnpj = "12345678912345"
        url = f"{mock_direct_data_api_requester.base_url}/api/CertidaoConjuntaDebitosPessoaJuridica"
        unexpected_json_response = {"message": "unexpected error"}
        
        route = respx.get(url=url).mock(
            return_value=Response(
                status_code=500, 
                json=unexpected_json_response
            )
        )

        with pytest.raises(UnexpectedError) as e:
            mock_direct_data_api_requester.get_certificado_url(cnpj)

        assert str(unexpected_json_response) in str(e.value)
        assert url in str(e.value)
        assert "500" in str(e.value)



        





