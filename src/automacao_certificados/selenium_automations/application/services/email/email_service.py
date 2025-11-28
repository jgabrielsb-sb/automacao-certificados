"""
Email Service.

This service encapsulates business logic for sending emails, including
validation, email preparation, and orchestration of email sending operations.
"""

from automacao_certificados.selenium_automations.core.interfaces.email_sender import EmailSenderPort
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailToSend


class EmailService:
    """
    Service for managing email operations with business logic.
    
    This service encapsulates the business logic for sending emails,
    including validation, email preparation, and error handling.
    It orchestrates the email sending adapter to accomplish business operations.
    """
    
    def __init__(self, email_sender: EmailSenderPort):
        """
        Initialize email service.
        """
        self.email_sender = email_sender
    
    def send_email(self, email: EmailToSend) -> None:
        """
        Send an email with business logic validation.
        
        :param email: The email to send, containing header and content information.
        :type email: EmailToSend
        """
        self.email_sender.send_email(email)