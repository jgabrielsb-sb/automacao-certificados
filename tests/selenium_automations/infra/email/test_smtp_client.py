# tests/infra/test_smtp_client.py

import pytest
from unittest.mock import patch, MagicMock

from automacao_certificados.selenium_automations.infra.email.smtp_client import SMTPClient
from automacao_certificados.selenium_automations.core.models.infra.dto_email import (
    EmailConfig,
    EmailToSend,
    EmailHeader,
    EmailContent,
)

@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.build_mime_multipart_email")
@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.smtplib.SMTP")
def test_send_email_with_tls_success(mock_smtp_cls, mock_build_email):
    # --- Arrange ---
    email_config = EmailConfig(
        email_host="smtp.test",
        email_port=587,
        email_host_user="user@test.com",
        email_host_password="secret",
        is_tls=True,
    )
    client = SMTPClient(email_config)

    # fake MIME message
    fake_mime = MagicMock()
    fake_mime.__getitem__.side_effect = lambda key: {
        "From": "user@test.com",
        "To": "dest@test.com",
    }[key]

    fake_mime.as_string.return_value = "RAW MIME STRING"
    mock_build_email.return_value = fake_mime

    # mock SMTP instance used as context manager
    mock_smtp_instance = mock_smtp_cls.return_value
    mock_smtp_instance.__enter__.return_value = mock_smtp_instance

    email_to_send = EmailToSend(
        email_header=EmailHeader(
            recipient_email=["dest@test.com"],
            sender_email="user@test.com"
        ),
        email_content=EmailContent(
            subject="Subject",
            is_html=True,
            body="Body"
        )
    )

    # --- Act ---
    client.send_email(email_to_send)

    # --- Assert ---

    # 1. SMTP created with correct host (and maybe port)
    mock_smtp_cls.assert_called_once_with(host="smtp.test", port=587)

    # 2. TLS started
    mock_smtp_instance.starttls.assert_called_once()

    # 3. Logged in with correct credentials
    mock_smtp_instance.login.assert_called_once_with(email_config.email_host_user, email_config.email_host_password)

    # 4. build_mime_multipart_email was called correctly
    mock_build_email.assert_called_once_with(email_to_send)

    # 5. sendmail was called with the MIME content
    mock_smtp_instance.sendmail.assert_called_once_with(
        from_addr=email_config.email_host_user,
        to_addrs=", ".join(email_to_send.email_header.recipient_email),
        msg=mock_build_email.return_value.as_string(),
    )

@patch("automacao_certificados.selenium_automations.infra.email.utils.build_mime_multipart_email")
@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.smtplib.SMTP")
def test_send_email_without_tls(mock_smtp_cls, mock_build_email):
    email_config = EmailConfig(
        email_host="smtp.test",
        email_port=25,
        email_host_user="user@test.com",
        email_host_password="secret",
        is_tls=False,
    )
    client = SMTPClient(email_config)

    fake_mime = MagicMock()
    fake_mime.__getitem__.side_effect = lambda key: {
        "From": "user@test.com",
        "To": "dest@test.com",
    }[key]
    fake_mime.as_string.return_value = "RAW MIME STRING"
    mock_build_email.return_value = fake_mime

    mock_smtp_instance = mock_smtp_cls.return_value
    mock_smtp_instance.__enter__.return_value = mock_smtp_instance

    email_to_send = EmailToSend(
        email_header=EmailHeader(
            recipient_email=["dest@test.com"],
            sender_email="user@test.com"
        ),
        email_content=EmailContent(
            subject="Subject",
            is_html=True,
            body="Body"
        )
    )

    client.send_email(email_to_send)

    # should NOT call starttls
    mock_smtp_instance.starttls.assert_not_called()

    # but should still login and sendmail
    mock_smtp_instance.login.assert_called_once_with(email_config.email_host_user, email_config.email_host_password)
    mock_smtp_instance.sendmail.assert_called_once()

from smtplib import SMTPConnectError
from automacao_certificados.selenium_automations.core.exceptions.infra.email_exceptions import (
    EmailConnectionException,
)

@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.smtplib.SMTP")
def test_get_smtp_raises_email_connection_exception(mock_smtp_cls):
    # make the constructor raise SMTPConnectError
    mock_smtp_cls.side_effect = SMTPConnectError(code=421, msg="cannot connect")

    email_config = EmailConfig(
        email_host="smtp.test",
        email_port=25,
        email_host_user="user@test.com",
        email_host_password="secret",
        is_tls=False,
    )
    client = SMTPClient(email_config)

    with pytest.raises(EmailConnectionException) as exc:
        client.connect_smtp()

    assert "error on email connection" in str(exc.value)

from smtplib import SMTPNotSupportedError
from automacao_certificados.selenium_automations.core.exceptions.infra.email_exceptions import (
    EmailTLSConnectionException,
)

@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.smtplib.SMTP")
def test_connect_tls_raises_email_tls_exception(mock_smtp_cls):
    email_config = EmailConfig(
        email_host="smtp.test",
        email_port=587,
        email_host_user="user@test.com",
        email_host_password="secret",
        is_tls=True,
    )
    client = SMTPClient(email_config)

    mock_smtp_instance = mock_smtp_cls.return_value
    mock_smtp_instance.starttls.side_effect = SMTPNotSupportedError("no tls")

    with pytest.raises(EmailTLSConnectionException):
        client.connect_smtp()

from smtplib import SMTPAuthenticationError
from automacao_certificados.selenium_automations.core.exceptions.infra.email_exceptions import (
    EmailLoginException,
)

@patch("automacao_certificados.selenium_automations.infra.email.smtp_client.smtplib.SMTP")
def test_login_raises_email_login_exception(mock_smtp_cls):
    email_config = EmailConfig(
        email_host="smtp.test",
        email_port=587,
        email_host_user="user@test.com",
        email_host_password="wrong",
        is_tls=False,
    )
    client = SMTPClient(email_config)

    mock_smtp_instance = mock_smtp_cls.return_value
    mock_smtp_instance.login.side_effect = SMTPAuthenticationError(535, b"auth failed")

    with pytest.raises(EmailLoginException):
        client.connect_smtp()




        
        