
from unittest import mock
import pytest
from unittest.mock import MagicMock, Mock

from automacao_certificados.selenium_automations.adapters.persistance.certificado_api_persistance import CertificadoApiPersistance
from automacao_certificados.selenium_automations.application.use_cases import DownloadCertificatesUseCase
from automacao_certificados.selenium_automations.application.workflow.factories.base_workflow_factory import WorkflowFactory
from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.core.exceptions.application.services.logging_register_service_exceptions import LoggingRegisterServiceException
from automacao_certificados.selenium_automations.core.exceptions.application.workflow_selector_exceptions import WorkflowSelectorException
from automacao_certificados.selenium_automations.core.interfaces.document_downloader import DocumentDownloaderPort
from automacao_certificados.selenium_automations.core.models.adapters.api_requester.dto_ppe_api import CertificateToDownload, DocumentTypeEnum
from automacao_certificados.selenium_automations.core.models.application.use_cases.dto_download_certificate_use_case import DownloadCertificateResult
from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import StepResult, WorkflowOutput
from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester
from automacao_certificados.selenium_automations.application.workflow.workflow_selector import WorkflowSelector
from automacao_certificados.selenium_automations.application.services import LoggingRegisterService
from automacao_certificados.selenium_automations.adapters import HttpxClient
from automacao_certificados.selenium_automations.core.interfaces import LoggingRegisterPort, MunicipioGetterPort, EstadoGetterPort
from automacao_certificados.selenium_automations.adapters import PPEPersistance

@pytest.fixture
def mock_download_certificate_use_case():
    return DownloadCertificatesUseCase(
        ppe_api_requester=MagicMock(spec=PPEAPIRequester),
        workflow_selector=MagicMock(spec=WorkflowSelector),
        logging_register_service=MagicMock(spec=LoggingRegisterService)
        
    )

@pytest.fixture
def mock_certificate_to_download():
    return CertificateToDownload(
        cnpj="12345678912345",
        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
    )

@pytest.fixture
def mock_step_result():
    return StepResult(
        sucess=True,
        error_message=None
    )

@pytest.fixture
def mock_workflow_output(mock_step_result):
    return WorkflowOutput(
        download_output_result=mock_step_result,
        persistance_output_result=mock_step_result,
        ppe_output_result=mock_step_result,
    )
    
@pytest.fixture
def mock_download_certificate_result(
    mock_certificate_to_download,
    mock_workflow_output
):
    return DownloadCertificateResult(
        certificate=mock_certificate_to_download,
        error_selection=None,
        workflow_output=mock_workflow_output
    )

@pytest.fixture
def mock_workflow_selector():
    return WorkflowSelector(
        municipio_getter_port=MagicMock(spec=MunicipioGetterPort),
        estado_getter_port=MagicMock(spec=EstadoGetterPort)
    )

@pytest.fixture
def mock_workflow():
    return Workflow(
        document_downloader=MagicMock(spec=DocumentDownloaderPort),
        certificado_api_persistance=MagicMock(spec=CertificadoApiPersistance),
        ppe_api_persistance=MagicMock(spec=PPEPersistance)
    )
    
class TestDownloadCertificatesUseCase:
    def test_if_raises_value_error_if_ppe_api_requester_is_not_a_ppe_api_requester(self):
        with pytest.raises(ValueError) as e:
            DownloadCertificatesUseCase(
                ppe_api_requester="invalid",
                workflow_selector=MagicMock(spec=WorkflowSelector),
                logging_register_service=MagicMock(spec=LoggingRegisterService)
            )
        
        assert "ppe_api_requester must be a PPEAPIRequester" in str(e.value)
    
    def test_if_raises_value_error_if_workflow_selector_is_not_a_workflow_selector(self):
        with pytest.raises(ValueError) as e:
            DownloadCertificatesUseCase(
                ppe_api_requester=MagicMock(spec=PPEAPIRequester),
                workflow_selector="invalid",
                logging_register_service=MagicMock(spec=LoggingRegisterService)
            )
        
        assert "workflow_selector must be a WorkflowSelector" in str(e.value)

    def test_if_raises_value_error_if_logging_register_service_is_not_a_logging_register_service(self):
        with pytest.raises(ValueError) as e:
            DownloadCertificatesUseCase(
                ppe_api_requester=MagicMock(spec=PPEAPIRequester),
                workflow_selector=MagicMock(spec=WorkflowSelector),
                logging_register_service="invalid"
            )
        
        assert "logging_register_service must be a LoggingRegisterService" in str(e.value)

class TestRegisterDownloadCertificatesCronExecution:
    def test_if_register_download_certificates_cron_execution_raises_value_error_if_not_a_list(
        self,
        mock_download_certificate_use_case: DownloadCertificatesUseCase,
    ):
        with pytest.raises(ValueError) as e:
            mock_download_certificate_use_case._register_download_certificates_cron_execution(
                certificates_to_download='not a list'
            )

        assert "certificates_to_download must be a list" in str(e.value)

    def test_if_register_download_certificates_cron_execution_raises_value_error_if_not_a_list_of_certificates_to_download(
        self,
        mock_download_certificate_use_case: DownloadCertificatesUseCase,
    ):
        with pytest.raises(ValueError) as e:
            mock_download_certificate_use_case._register_download_certificates_cron_execution(
                certificates_to_download=["list of wrong type"]
            )

        assert "all elements of certificates_to_download must be CertificateToDownload" in str(e.value)

    def test_if_when_logging_register_service_raises_exception_the_exception_does_not_bubble(
        self,
        monkeypatch,
        mock_certificate_to_download,
        mock_download_certificate_result,
        mock_download_certificate_use_case: DownloadCertificatesUseCase
    ):
        mock_logging_register_service = MagicMock(spec=LoggingRegisterService)
        mock_logging_register_service.register_download_certificates_cron_execution.side_effect = LoggingRegisterServiceException(
            message="test"
        )

        monkeypatch.setattr(
            mock_download_certificate_use_case,
            "logging_register_service",
            mock_logging_register_service
            )

        
        mock_download_certificate_use_case._register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=mock_download_certificate_result
        )
    
class TestDownloadCertificate:
    def test_if_raises_value_error_if_certificate_is_not_a_certificate_to_download(
        self,
        mock_download_certificate_use_case: DownloadCertificatesUseCase,
    ):
        with pytest.raises(ValueError) as e:
            mock_download_certificate_use_case._download_certificate(
                certificate="invalid"
            )
        
        assert "certificate must be a CertificateToDownload" in str(e.value)

    def test_if_returns_correct_result(
        self,
        monkeypatch,
        mock_workflow_selector: WorkflowSelector,
        mock_step_result: StepResult,
    ):
        # Arrange – create the certificate
        certificate = CertificateToDownload(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL,
        )

        # Mock dependencies
        mock_ppe_api_requester = MagicMock(spec=PPEAPIRequester)
        mock_workflow_selector = MagicMock(spec=WorkflowSelector)

        # Mock workflow and its run() return
        mock_workflow = Mock()
        mock_workflow.run.return_value = WorkflowOutput(
            download_output_result=mock_step_result,
            persistance_output_result=mock_step_result,
            ppe_output_result=mock_step_result
        )

        # When get_workflow is called, it returns the mock workflow
        mock_workflow_selector.get_workflow.return_value = mock_workflow

        use_case = DownloadCertificatesUseCase(
            ppe_api_requester=mock_ppe_api_requester,
            workflow_selector=mock_workflow_selector,
            logging_register_service=MagicMock(spec=LoggingRegisterService),
        )

        # Act
        result = use_case._download_certificate(certificate)

        assert result == DownloadCertificateResult(
            certificate=certificate,
            error_selection=None,
            workflow_output=WorkflowOutput(
            download_output_result=mock_step_result,
                persistance_output_result=mock_step_result,
                ppe_output_result=mock_step_result
            )
        )

    def test_if_returns_correct_result_when_error_on_selection(
        self,
        monkeypatch,
        mock_workflow_selector: WorkflowSelector,
        mock_step_result: StepResult,
    ):
        # Arrange – create the certificate
        certificate = CertificateToDownload(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL,
        )

        def fake_get_workflow(cnpj, document_type):
            raise WorkflowSelectorException(message="test")

        monkeypatch.setattr(mock_workflow_selector, "get_workflow", fake_get_workflow)

        use_case = DownloadCertificatesUseCase(
            ppe_api_requester=MagicMock(spec=PPEAPIRequester),
            workflow_selector=mock_workflow_selector,
            logging_register_service=MagicMock(spec=LoggingRegisterService),
        )

        # Act
        result = use_case._download_certificate(certificate)

        assert result == DownloadCertificateResult(
            certificate=certificate,
            error_selection="test",
            workflow_output=WorkflowOutput()
        )

class TestDownloadCertificates:
    def test_if_raises_value_error_if_certificates_to_download_is_not_a_list(
        self,
        mock_download_certificate_use_case: DownloadCertificatesUseCase,
    ):
        with pytest.raises(ValueError) as e:
            mock_download_certificate_use_case._download_certificates(
                certificates_to_download="not a list"
            )

        assert "certificates_to_download must be a list" in str(e.value)

    def test_if_raises_value_error_if_certificates_to_download_is_not_a_list_of_certificates_to_download(
        self,
        mock_download_certificate_use_case: DownloadCertificatesUseCase,
    ):
        with pytest.raises(ValueError) as e:
            mock_download_certificate_use_case._download_certificates(
                certificates_to_download=["not a list of certificates to download"]
            )

        assert "all elements of certificates_to_download must be CertificateToDownload" in str(e.value)
