import pytest
from automacao_certificados.selenium_automations.application.use_cases import SendDownloadCertificatesReportViaEmailUseCase
from automacao_certificados.selenium_automations.core.interfaces import EmailSenderPort


class TestSendDownloadCertificatesReportViaEmailUseCase:
    def test_if_raises_value_error_if_email_sender_is_not_email_sender_port_type(
        self
    ):
        with pytest.raises(ValueError) as e:
            SendDownloadCertificatesReportViaEmailUseCase(email_sender="none")
        
        assert "email_sender must be EmailSenderPort" in str(e.value)