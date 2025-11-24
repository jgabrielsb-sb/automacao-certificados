from _pytest import monkeypatch
from automacao_certificados.selenium_automations.application.use_cases import DownloadCertificatesUseCase
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import *

import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_use_case():
    return DownloadCertificatesUseCase(
        ppe_api_requester=Mock(spec=PPEAPIRequester),
        workflow_selector=Mock(WorkflowSelector)
    )

class TestInitDownloadCertificatesUseCase: 

    def test_if_ppe_api_requester_is_not_a_ppe_api_requester_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            DownloadCertificatesUseCase(
                ppe_api_requester=None,
                workflow_selector=WorkflowSelector(Mock(spec=MunicipioGetterPort))
            )

        assert "ppe_api_requester must be a PPEAPIRequester" in str(e.value)

    def test_if_workflow_selector_is_not_a_workflow_selector_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            DownloadCertificatesUseCase(
                ppe_api_requester=Mock(spec=PPEAPIRequester),
                workflow_selector=None
            )

        assert "workflow_selector must be a WorkflowSelector" in str(e.value)

class TestDownloadCertificate:
    def test_if_download_certificate_returns_correct_output_when_workflow_selector_exception(
        self,
        mock_use_case,
        monkeypatch,
    ):
        mock_workflow_selector = MagicMock()
        mock_workflow_selector.get_workflow.side_effect = WorkflowSelectorException(
            message="test message"
        )

        monkeypatch.setattr(mock_use_case, "workflow_selector", mock_workflow_selector)

        certificate = CertificateToDownload(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS
        )

        output = mock_use_case._download_certificate(certificate)
        assert output == DownloadCertificatesUseCaseOutput(
            certificate=certificate,
            error_selection="test message",
            workflow_output=WorkflowOutput()
        )

    def test_if_download_certificate_returns_correct_output_when_workflow_selector_selects_successfully(
        self,
        mock_use_case: DownloadCertificatesUseCase,
    ):
        # This is what the use case expects to eventually get:
        workflow_output = WorkflowOutput()

        # Mock the workflow instance
        mock_workflow = Mock()
        mock_workflow.run.return_value = workflow_output

        # Mock the selector and plug it into the use case
        mock_workflow_selector = Mock(spec=WorkflowSelector)
        mock_workflow_selector.get_workflow.return_value = mock_workflow

        # Attach to the use case (no need for monkeypatch)
        mock_use_case.workflow_selector = mock_workflow_selector

        certificate = CertificateToDownload(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS,
        )

        output = mock_use_case._download_certificate(certificate)

        assert output == DownloadCertificatesUseCaseOutput(
            certificate=certificate,
            error_selection=None,
            workflow_output=workflow_output,
        )

class TestRun:
    def test_if_run_is_wrapping_exceptions_on_download_certificate_use_case_exception(
        self,
        mock_use_case,
        monkeypatch
    ):
        def fake_get_certificates_to_download():
            raise Exception("test")

        monkeypatch.setattr(mock_use_case, "_get_certificates_to_download", fake_get_certificates_to_download)

        with pytest.raises(DownloadCertificatesUseCaseException) as e:
            mock_use_case.run()

        assert "test" in str(e.value)

    def test_if_run_returns_correct_output(
        self,
        mock_use_case,
        monkeypatch
    ):
        def fake_get_certificates_to_download():
            return "test"
        
        download_certificate_output = DownloadCertificatesUseCaseOutput(
            certificate=CertificateToDownload(
                cnpj="12345678912345",
                document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
            ),
            error_selection=None,
            workflow_output=WorkflowOutput(
                download_output_result=None,
                persistance_output_result=None,
                ppe_output_result=None,
            )
        )
        
        def fake_download_certificates(certificates_to_download):
            return [download_certificate_output]

        monkeypatch.setattr(mock_use_case, "_get_certificates_to_download", fake_get_certificates_to_download)
        monkeypatch.setattr(mock_use_case, "_download_certificates", fake_download_certificates)
        
        output = mock_use_case.run()
        assert output == [download_certificate_output]
        

        

        









        