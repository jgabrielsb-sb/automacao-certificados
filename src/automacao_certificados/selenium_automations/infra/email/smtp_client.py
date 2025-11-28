from automacao_certificados.selenium_automations.core.models import (
    EmailConfig,
    EmailToSend
)

from automacao_certificados.selenium_automations.core.exceptions.infra.email_exceptions import *
from .utils import build_mime_multipart_email

import smtplib

class SMTPClient:
    def __init__(self, email_config: EmailConfig):
        if not isinstance(email_config, EmailConfig):
            raise ValueError("email_config must be a EmailConfig type")

        self.email_config = email_config

    def _get_smtp(self) -> smtplib.SMTP:
        try:
            return smtplib.SMTP(
                host=self.email_config.email_host,
                port=self.email_config.email_port,  # if you have it
            )
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            raise EmailConnectionException(f"error on email connection: {e}")

    def _connect_tls(self, smtp: smtplib.SMTP) -> smtplib.SMTP:
        try:
            smtp.starttls()
            return smtp
        except smtplib.SMTPNotSupportedError as e:
            raise EmailTLSConnectionException(
                f"error on trying to establish smtp connection: {e}"
            )

    def _login_smtp(self, smtp: smtplib.SMTP) -> smtplib.SMTP:
        try:
            smtp.login(self.email_config.email_host_user, self.email_config.email_host_password)
            return smtp
        except smtplib.SMTPAuthenticationError as e:
            raise EmailLoginException(f"error while logging in: {e}")
    
    def connect_smtp(self) -> smtplib.SMTP:
        smtp = self._get_smtp()
        
        if self.email_config.is_tls:
            smtp = self._connect_tls(smtp)
        
        smtp = self._login_smtp(smtp)
        return smtp

    def send_email(self, email: EmailToSend) -> None:
        email_mime = build_mime_multipart_email(email)
        print('called build_mime_multipart_email')

        with self.connect_smtp() as smtp:
            try:
                smtp.sendmail(
                    from_addr=email_mime["From"],
                    to_addrs=email_mime["To"],
                    msg=email_mime.as_string(),
                )
            except Exception as e:
                raise EmailSendException(f"error while sending email: {e}")
