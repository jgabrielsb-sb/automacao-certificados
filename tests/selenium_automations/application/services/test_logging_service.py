import pytest

from unittest.mock import MagicMock
from datetime import datetime

from automacao_certificados.selenium_automations.adapters.persistance import ppe_persistance
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

@pytest.fixture
def mock_certificate_to_download():
    return CertificateToDownload(
        cnpj="12345678912345",
        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
    )

class TestLoggingService:
    def test_if_raises_value_error_if_logging_register_port_is_not_a_logging_register_port(self):
        with pytest.raises(ValueError) as e:
            LoggingRegisterService(
                logging_register="invalid"
            )

        assert "logging_register must be a LoggingRegisterPort" in str(e.value)

class TestRegisterDownloadCertificatesCronExecution:
    def test_if_raises_value_error_if_input_is_not_a_register_download_certificates_cron_execution(self):
        with pytest.raises(ValueError) as e:
            LoggingRegisterService(
                logging_register=MagicMock(spec=LoggingRegisterPort)
            ).register_download_certificates_cron_execution(
                input="invalid"
            )

        assert "input must be a RegisterDownloadCertificatesCronExecution" in str(e.value)

    def test_convert_register_download_certificates_cron_execution_to_logging_register_input(
        self,
        mock_certificate_to_download
    ) -> LoggingRegisterInput:
        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.return_value = None

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        datetime_now = datetime.now()
        register_download_certificates_cron_execution = RegisterDownloadCertificatesCronExecution(
            certificates_to_download=[mock_certificate_to_download],
            cron_datetime=datetime_now
        )

        logging_register_input = logging_register_service._convert_register_download_certificates_cron_execution_to_logging_register_input(
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
        mock_certificate_to_download
    ):
        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.return_value = None

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        logging_register_service.register_download_certificates_cron_execution(
            input=RegisterDownloadCertificatesCronExecution(
                certificates_to_download=[mock_certificate_to_download],
                cron_datetime=datetime.now()
            )
        )

    def test_if_register_download_certificates_cron_execution_is_being_wrapped_on_proper_exeption(
        self,
        mock_certificate_to_download
    ):
        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message="test"
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        register_download_certificates_cron_execution = RegisterDownloadCertificatesCronExecution(
            certificates_to_download=[mock_certificate_to_download],
            cron_datetime=datetime.now()
        )

        with pytest.raises(LoggingRegisterServiceException) as e:
            logging_register_service.register_download_certificates_cron_execution(
                input=register_download_certificates_cron_execution
            )

        assert f"error on registering logging of download certificates cron execution" in str(e.value)
        assert "test" in str(e.value)

class TestRegisterDownloadCertificateResult:
    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_selection(
        self,
        mock_certificate_to_download
    ):
        download_datetime = datetime.now()

        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message="test"
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        download_certificate_result = DownloadCertificateResult(
            certificate=mock_certificate_to_download,
            error_selection="error on selection",
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
                persistance_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
            )
        )
        
        error_on_selection = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service._convert_register_download_certificate_result_to_logging_register_input(
            error_on_selection
        )

        assert logging_register_input == LoggingRegisterInput(
            timestamp=download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message="A request to download a certificate has been registered. Check 'details' for more information.",
            level=Level.INFO,
            status=Status.FAILURE,
            details={
                "certificate_to_download": mock_certificate_to_download,
                "result": download_certificate_result
            }
        )

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_download(
        self,
        mock_certificate_to_download
    ):
        download_datetime = datetime.now()

        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message="test"
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        download_certificate_result = DownloadCertificateResult(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
                persistance_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
            )
        )
        
        error_on_selection = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service._convert_register_download_certificate_result_to_logging_register_input(
            error_on_selection
        )

        assert logging_register_input == LoggingRegisterInput(
            timestamp=download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message="A request to download a certificate has been registered. Check 'details' for more information.",
            level=Level.INFO,
            status=Status.FAILURE,
            details={
                "certificate_to_download": mock_certificate_to_download,
                "result": download_certificate_result
            }
        )

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_api_persistance(
        self,
        mock_certificate_to_download
    ):
        download_datetime = datetime.now()

        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message="test"
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        download_certificate_result = DownloadCertificateResult(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=True,
                    error_message=None
                ),
                persistance_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message="error on download"
                ),
            )
        )
        
        error_on_selection = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service._convert_register_download_certificate_result_to_logging_register_input(
            error_on_selection
        )

        assert logging_register_input == LoggingRegisterInput(
            timestamp=download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message="A request to download a certificate has been registered. Check 'details' for more information.",
            level=Level.INFO,
            status=Status.PARTIAL,
            details={
                "certificate_to_download": mock_certificate_to_download,
                "result": download_certificate_result
            }
        )

    def test_if_convert_register_download_certificate_result_to_logging_result_return_correct_logging_register_input_when_error_on_ppe_persistance(
        self,
        mock_certificate_to_download
    ):
        download_datetime = datetime.now()

        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message="test"
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        download_certificate_result = DownloadCertificateResult(
            certificate=mock_certificate_to_download,
            error_selection=None,
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=True,
                    error_message=None
                ),
                persistance_output_result=StepResult(
                    sucess=True,
                    error_message=None
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message="error on ppe persistance"
                ),
            )
        )
        
        error_on_selection = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_certificate_result=download_certificate_result,
            download_datetime=download_datetime
        )

        logging_register_input = logging_register_service._convert_register_download_certificate_result_to_logging_register_input(
            error_on_selection
        )

        assert logging_register_input == LoggingRegisterInput(
            timestamp=download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message="A request to download a certificate has been registered. Check 'details' for more information.",
            level=Level.INFO,
            status=Status.PARTIAL,
            details={
                "certificate_to_download": mock_certificate_to_download,
                "result": download_certificate_result
            }
        )

    def test_sucess_register_download_certificate_result(
        self,
        mock_certificate_to_download,
    ): 
        download_datetime = datetime.now()
        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.return_value = None

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        input = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_datetime=datetime.now(),
            download_certificate_result=DownloadCertificateResult(
                certificate=mock_certificate_to_download,
                error_selection=None,
                workflow_output=WorkflowOutput(
                    download_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    ),
                    persistance_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    ),
                    ppe_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    )
                )
            )
        )

        logging_register_service.register_download_certificate_result(input)

    def test_if_register_download_certificate_result_is_being_wrapped_on_proper_exception(
        self,
        mock_certificate_to_download,
    ): 
        mock_logging_register = MagicMock(spec=LoggingRegisterPort)
        mock_logging_register.run.side_effect = LoggingRegisterException(
            message='test'
        )

        logging_register_service = LoggingRegisterService(
            logging_register=mock_logging_register
        )

        input = RegisterDownloadCertificateResult(
            certificate_to_download=mock_certificate_to_download,
            download_datetime=datetime.now(),
            download_certificate_result=DownloadCertificateResult(
                certificate=mock_certificate_to_download,
                error_selection=None,
                workflow_output=WorkflowOutput(
                    download_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    ),
                    persistance_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    ),
                    ppe_output_result=StepResult(
                        sucess=True,
                        error_message=None
                    )
                )
            )
        )

        with pytest.raises(LoggingRegisterServiceException) as e:
            logging_register_service.register_download_certificate_result(input)

        assert "error on registering logging of download certificate" in str(e.value)
        assert "test" in str(e.value)




        

        








    