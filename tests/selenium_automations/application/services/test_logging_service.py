import pytest

from unittest.mock import MagicMock
from datetime import datetime

from automacao_certificados.selenium_automations.application.services import LoggingRegisterService
from automacao_certificados.selenium_automations.core.interfaces import LoggingRegisterPort
from automacao_certificados.selenium_automations.core.models import RegisterDownloadCertificatesCronExecution
from automacao_certificados.selenium_automations.core.models.adapters.api_requester.dto_ppe_api import CertificateToDownload, DocumentTypeEnum
from automacao_certificados.selenium_automations.core.models.interfaces.dto_logging_register import LoggingRegisterInput
from automacao_certificados.selenium_automations.core.models.enum_level import Level
from automacao_certificados.selenium_automations.core.models.enum_status import Status

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

    