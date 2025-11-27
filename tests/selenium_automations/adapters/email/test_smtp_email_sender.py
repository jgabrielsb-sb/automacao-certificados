import pytest
from unittest.mock import patch

from automacao_certificados.selenium_automations.adapters.email.smtp_email_sender import SMTPEmailSender
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailConfig
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailToSend
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailHeader
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailContent

@pytest.fixture
def email_config():
    return EmailConfig(
        email_host="smtp.test",
        email_port=587,
        email_host_user="user@test.com",
        email_host_password="secret",
        is_tls=True,
    )
class TestSMTPEmailSender:
    def test_if_raises_value_error_if_email_config_is_not_email_config_type(
        self
    ):
        with pytest.raises(ValueError) as e:
            SMTPEmailSender(email_config="none")
        
        assert "email_config must be a EmailConfig type" in str(e.value)

    def test_if_raises_value_error_if_email_is_not_email_to_send_type(
        self,
        email_config
    ):
        with pytest.raises(ValueError) as e:
            SMTPEmailSender(email_config=email_config).send_email(email="none")
        
        assert "email must be a EmailToSend type" in str(e.value)
