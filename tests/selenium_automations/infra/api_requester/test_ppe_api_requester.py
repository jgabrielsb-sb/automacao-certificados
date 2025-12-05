
import pytest
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester

@pytest.fixture
def ppe_api_requester():
    return PPEAPIRequester(
        http=HttpxClient(),
        api_key='test_api_key'
    )

class TestPPEAPIRequester:
    def test_convert_response_to_certificates_to_download(self):
        mock_response_data = [
            {
            'cnpj': '14868712000131', 
            'nome': 'Akad Seguros S A', 
            'certificates': 
                [
                    'Certidão Negativa Federal', 
                    'Certidão Negativa FGTS'
                ]
            }, 
            {
                'cnpj': '04740876000125', 
                'nome': 'Alelo S A', 
                'certificates': 
                    [
                        'Certidão Negativa Federal', 
                        'Certidão Negativa FGTS', 
                        'Certidão Negativa Municipal'
                    ]
            }
        ]

        expected_certificates_to_download = [
            CertificateToDownload(cnpj='14868712000131', document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL),
            CertificateToDownload(cnpj='14868712000131', document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS),
            CertificateToDownload(cnpj='04740876000125', document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL),
            CertificateToDownload(cnpj='04740876000125', document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS),
            CertificateToDownload(cnpj='04740876000125', document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL),
        ]

        ppe_api_requester = PPEAPIRequester(
            http=HttpxClient(),
            api_key='test_api_key'
        )

        certificates_to_download = ppe_api_requester._convert_response_to_certificates_to_download(mock_response_data)
        assert certificates_to_download == expected_certificates_to_download

        
        