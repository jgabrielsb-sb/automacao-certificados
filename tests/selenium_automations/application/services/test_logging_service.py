import pytest

from unittest.mock import MagicMock
from datetime import datetime

from automacao_certificados.selenium_automations.application.services import LoggingRegisterService
from automacao_certificados.selenium_automations.core.exceptions.interfaces.exceptions import LoggingRegisterException
from automacao_certificados.selenium_automations.core.exceptions.application.services import LoggingRegisterServiceException
from automacao_certificados.selenium_automations.core.interfaces import LoggingRegisterPort
from automacao_certificados.selenium_automations.core.models import RegisterDownloadCertificatesCronExecution
from automacao_certificados.selenium_automations.core.models.adapters.api_requester.dto_ppe_api import CertificateToDownload, DocumentTypeEnum
from automacao_certificados.selenium_automations.core.models.application.services.dto_logging_register_service import RegisterDownloadCertificateResult
from automacao_certificados.selenium_automations.core.models.application.use_cases.dto_download_certificate_use_case import DownloadCertificateResult
from automacao_certificados.selenium_automations.core.models.interfaces.dto_logging_register import LoggingRegisterInput
from automacao_certificados.selenium_automations.core.models.enum_level import Level
from automacao_certificados.selenium_automations.core.models.enum_status import Status
from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import StepResult, WorkflowOutput


# Fixtures
@pytest.fixture
def mock_certificate_to_download():
    return CertificateToDownload(
        cnpj="12345678912345",
        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
    )


@pytest.fixture
def mock_logging_register_success():
    mock = MagicMock(spec=LoggingRegisterPort)
    mock.run.return_value = None
    return mock


@pytest.fixture
def mock_logging_register_error():
    mock = MagicMock(spec=LoggingRegisterPort)
    mock.run.side_effect = LoggingRegisterException(message="test")
    return mock


@pytest.fixture
def logging_register_service_success(mock_logging_register_success):
    return LoggingRegisterService(logging_register=mock_logging_register_success)


@pytest.fixture
def logging_register_service_error(mock_logging_register_error):
    return LoggingRegisterService(logging_register=mock_logging_register_error)


# Helper functions
def create_step_result(success: bool, error_message: str | None = None) -> StepResult:
    """Helper to create StepResult objects."""
    return StepResult(sucess=success, error_message=error_message)


def create_workflow_output(
    download_success: bool = True,
    persistance_success: bool = True,
    ppe_success: bool = True,
    download_error: str | None = None,
    persistance_error: str | None = None,
    ppe_error: str | None = None
) -> WorkflowOutput:
    """Helper to create WorkflowOutput objects with configurable step results."""
    return WorkflowOutput(
        download_output_result=create_step_result(download_success, download_error),
        persistance_output_result=create_step_result(persistance_success, persistance_error),
        ppe_output_result=create_step_result(ppe_success, ppe_error)
    )


def create_download_certificate_result(
    certificate: CertificateToDownload,
    error_selection: str | None = None,
    workflow_output: WorkflowOutput | None = None
) -> DownloadCertificateResult:
    """Helper to create DownloadCertificateResult objects."""
    if workflow_output is None:
        workflow_output = create_workflow_output()
    
    return DownloadCertificateResult(
        certificate=certificate,
        error_selection=error_selection,
        workflow_output=workflow_output
    )


def create_register_download_certificate_result(
    certificate_to_download: CertificateToDownload,
    download_certificate_result: DownloadCertificateResult,
    download_datetime: datetime | None = None
) -> RegisterDownloadCertificateResult:
    """Helper to create RegisterDownloadCertificateResult objects."""
    if download_datetime is None:
        download_datetime = datetime.now()
    
    return RegisterDownloadCertificateResult(
        certificate_to_download=certificate_to_download,
        download_certificate_result=download_certificate_result,
        download_datetime=download_datetime
    )


def create_expected_logging_register_input_for_download_certificate(
    timestamp: datetime,
    certificate_to_download: CertificateToDownload,
    download_certificate_result: DownloadCertificateResult,
    status: Status
) -> LoggingRegisterInput:
    """Helper to create expected LoggingRegisterInput for download certificate tests."""
    return LoggingRegisterInput(
        timestamp=timestamp,
        facility="automacao",
        event_name="download_certificate",
        message="A request to download a certificate has been registered. Check 'details' for more information.",
        level=Level.INFO,
        status=status,
        details={
            "certificate_to_download": certificate_to_download,
            "result": download_certificate_result
        }
    )

class TestLoggingService:
    def test_if_raises_value_error_if_logging_register_port_is_not_a_logging_register_port(self):
        with pytest.raises(ValueError) as e:
            LoggingRegisterService(logging_register="invalid")

        assert "logging_register must be a LoggingRegisterPort" in str(e.value)

class TestRegisterDownloadCertificatesCronExecution:
    def test_if_raises_value_error_if_input_is_not_a_register_download_certificates_cron_execution(
        self,
        logging_register_service_success
    ):
        with pytest.raises(ValueError) as e:
            logging_register_service_success.register_download_certificates_cron_execution(
                input="invalid"
            )

        assert "input must be a RegisterDownloadCertificatesCronExecution" in str(e.value)

    def test_convert_register_download_certificates_cron_execution_to_logging_register_input(
        self,
        mock_certificate_to_download,
        logging_register_service_success
    ):
        datetime_now = datetime.now()
        register_download_certificates_cron_execution = RegisterDownloadCertificatesCronExecution(
            certificates_to_download=[mock_certificate_to_download],
            cron_datetime=datetime_now
        )

        logging_register_input = logging_register_service_success._convert_register_download_certificates_cron_execution_to_logging_register_input(
            input=register_download_certificates_cron_execution
        )
         
        expected_output = LoggingRegisterInput(
            timestamp=datetime_now,
            facility="automacao",
            event_name="download_certificates_cron_execution",
            level=Level.INFO,
            status=Status.SUCCESS,
            message="""The routine to download the necessary certificates given PPE API response has been executed. Check 'details' for informations about the certificates that has been requested to download.""",
            details={"requested_certificates": [mock_certificate_to_download]}
        )
        assert isinstance(logging_register_input, LoggingRegisterInput)
        assert logging_register_input == expected_output
        
    def test_sucess_register_download_certificates_cron_execution(
        self,
        mock_certificate_to_download,
        logging_register_service_success
    ):
        logging_register_service_success.register_download_certificates_cron_execution(
            input=RegisterDownloadCertificatesCronExecution(
                certificates_to_download=[mock_certificate_to_download],
                cron_datetime=datetime.now()
            )
        )

    def test_if_register_download_certificates_cron_execution_is_being_wrapped_on_proper_exeption(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ):
        register_download_certificates_cron_execution = RegisterDownloadCertificatesCronExecution(
            certificates_to_download=[mock_certificate_to_download],
            cron_datetime=datetime.now()
        )

        with pytest.raises(LoggingRegisterServiceException) as e:
            logging_register_service_error.register_download_certificates_cron_execution(
                input=register_download_certificates_cron_execution
            )

        assert "error on registering logging of download certificates cron execution" in str(e.value)
        assert "test" in str(e.value)

class TestRegisterDownloadCertificateResult:
    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_selection(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ):
        download_datetime = datetime.now()
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection="error on selection",
            workflow_output=create_workflow_output(
                download_success=False,
                persistance_success=False,
                ppe_success=False,
                download_error="error on download",
                persistance_error="error on download",
                ppe_error="error on download"
            )
        )
        
        register_result = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service_error._convert_register_download_certificate_result_to_logging_register_input(
            register_result
        )

        expected = create_expected_logging_register_input_for_download_certificate(
            timestamp=download_datetime,
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            status=Status.FAILURE
        )
        assert logging_register_input == expected

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_download(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ):
        download_datetime = datetime.now()
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=create_workflow_output(
                download_success=False,
                persistance_success=False,
                ppe_success=False,
                download_error="error on download",
                persistance_error="error on download",
                ppe_error="error on download"
            )
        )
        
        register_result = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service_error._convert_register_download_certificate_result_to_logging_register_input(
            register_result
        )

        expected = create_expected_logging_register_input_for_download_certificate(
            timestamp=download_datetime,
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            status=Status.FAILURE
        )
        assert logging_register_input == expected

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_api_persistance(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ):
        download_datetime = datetime.now()
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=create_workflow_output(
                download_success=True,
                persistance_success=False,
                ppe_success=False,
                persistance_error="error on download",
                ppe_error="error on download"
            )
        )
        
        register_result = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service_error._convert_register_download_certificate_result_to_logging_register_input(
            register_result
        )

        expected = create_expected_logging_register_input_for_download_certificate(
            timestamp=download_datetime,
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            status=Status.PARTIAL
        )
        assert logging_register_input == expected

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_ppe_persistance(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ):
        download_datetime = datetime.now()
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=create_workflow_output(
                download_success=True,
                persistance_success=True,
                ppe_success=False,
                ppe_error="error on ppe persistance"
            )
        )
        
        register_result = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service_error._convert_register_download_certificate_result_to_logging_register_input(
            register_result
        )

        expected = create_expected_logging_register_input_for_download_certificate(
            timestamp=download_datetime,
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            status=Status.PARTIAL
        )
        assert logging_register_input == expected

    def test_sucess_register_download_certificate_result(
        self,
        mock_certificate_to_download,
        logging_register_service_success
    ): 
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=create_workflow_output()
        )
        
        input_data = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result
        )

        logging_register_service_success.register_download_certificate_result(input_data)

    def test_if_register_download_certificate_result_is_being_wrapped_on_proper_exception(
        self,
        mock_certificate_to_download,
        logging_register_service_error
    ): 
        download_certificate_result = create_download_certificate_result(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=create_workflow_output()
        )
        
        input_data = create_register_download_certificate_result(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result
        )

        with pytest.raises(LoggingRegisterServiceException) as e:
            logging_register_service_error.register_download_certificate_result(input_data)

        assert "error on registering logging of download certificate" in str(e.value)
        assert "test" in str(e.value)





    