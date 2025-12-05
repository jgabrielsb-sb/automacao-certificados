
from automacao_certificados.selenium_automations.core.exceptions.application.services.logging_register_service_exceptions import LoggingRegisterServiceException
from automacao_certificados.selenium_automations.core.interfaces import (
    LoggingRegisterPort,
    logging_register
)

from automacao_certificados.selenium_automations.core.models import (
    RegisterDownloadCertificatesCronExecution,
    RegisterDownloadCertificateResult,
    Level,
    Status
)

from automacao_certificados.selenium_automations.core.exceptions import (
    LoggingRegisterException
)
from automacao_certificados.selenium_automations.core.models.interfaces.dto_logging_register import LoggingRegisterInput

class LoggingRegisterService:
    def __init__(self, logging_register: LoggingRegisterPort):
        if not isinstance(logging_register, LoggingRegisterPort):
            raise ValueError("logging_register must be a LoggingRegisterPort")

        self.logging_register = logging_register

    def _convert_register_download_certificates_cron_execution_to_logging_register_input(
        self,
        input: RegisterDownloadCertificatesCronExecution
    ) -> LoggingRegisterInput:
        message = """The routine to download the necessary certificates given PPE API response has been executed. Check 'details' for informations about the certificates that has been requested to download."""

        logging_register_input = LoggingRegisterInput(
            timestamp=input.cron_datetime,
            facility="automacao",
            event_name="download_certificates_cron_execution",
            level=Level.INFO,
            status=Status.SUCCESS,
            message=message,
            details={"requested_certificates": input.certificates_to_download}
        )

        return logging_register_input


    def register_download_certificates_cron_execution(
        self, 
        input: RegisterDownloadCertificatesCronExecution
    ):
        """
        Must register the execution of a cron.
        The main information that must be registered is the certificates that
        must be downloaded.

        :param input: the necessary parameters to register the execution of a cron
        :type input: RegisterCronExecution

        :return: none
        :rtype: None
        """
        if not isinstance(input, RegisterDownloadCertificatesCronExecution):
            raise ValueError("input must be a RegisterDownloadCertificatesCronExecution")
        
        logging_register_input = self._convert_register_download_certificates_cron_execution_to_logging_register_input(input)

        try:
            self.logging_register.run(logging_register_input)
        except LoggingRegisterException as e:
            raise LoggingRegisterServiceException(
                f"error on registering logging of download certificates cron execution. Original Exception: {e}"
            )

    def _convert_register_download_certificate_result_to_logging_register_input(
        self,
        input:RegisterDownloadCertificateResult
    ) -> LoggingRegisterInput:
        message = "A request to download a certificate has been registered. Check 'details' for more information."
        status = (
            input.download_certificate_result.workflow_output.sucess 
            if (not input.download_certificate_result.error_selection) else 
            Status.FAILURE
        )

        logging_register_input = LoggingRegisterInput(
            timestamp=input.download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message=message,
            level=Level.INFO,
            status=status,
            details={
                "certificate_to_download": input.certificate_to_download,
                "result": input.download_certificate_result
            }
        )

        return logging_register_input

    def register_download_certificate_result(
        self,
        input: RegisterDownloadCertificateResult,
    ):
        message = "A request to download a certificate has been registered. Check 'details' for more information."
        status = (
            input.download_certificate_result.workflow_output.sucess 
            if (not input.download_certificate_result.error_selection) else 
            Status.FAILURE
        )
        logging_register_input = LoggingRegisterInput(
            timestamp=input.download_datetime,
            facility="automacao",
            event_name="download_certificate",
            message=message,
            level=Level.INFO,
            status=status,
            details={
                "certificate_to_download": input.certificate_to_download,
                "result": input.download_certificate_result
            }
        )

        try:
            self.logging_register.run(logging_register_input)
        except LoggingRegisterException as e:
            raise LoggingRegisterServiceException(
                f"error on registering logging of download certificate. Original Exception: {e}"
            )