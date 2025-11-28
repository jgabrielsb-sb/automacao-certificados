"""
SMTP Email Sender Adapter.

This adapter implements the EmailSenderPort interface using SMTP protocol.
It wraps the SMTPClient infrastructure component to provide email sending
functionality to the application layer.
"""

from automacao_certificados.selenium_automations.core.interfaces.email_sender import EmailSenderPort
from automacao_certificados.selenium_automations.core.models.infra.dto_email import (
    EmailConfig,
    EmailToSend
)
from automacao_certificados.selenium_automations.infra.email.smtp_client import SMTPClient


class SMTPEmailSender(EmailSenderPort):
    """
    Adapter for sending emails via SMTP.
    
    This adapter implements the EmailSenderPort interface and uses the
    SMTPClient infrastructure component to send emails.
    """
    
    def __init__(self, email_config: EmailConfig):
        """
        Initialize SMTP email sender adapter.
        """
        if not isinstance(email_config, EmailConfig):
            raise ValueError("email_config must be a EmailConfig type")

        self.smtp_client = SMTPClient(email_config)
    
    def send_email(self, email: EmailToSend) -> None:
        """
        Send an email via SMTP.
        
        :param email: The email to send, containing header and content information.
        :type email: EmailToSend
        :return: None
        :rtype: None
        """
        if not isinstance(email, EmailToSend):
            raise ValueError("email must be a EmailToSend type")

        self.smtp_client.send_email(email)

