from typing import Protocol, runtime_checkable

from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailToSend

@runtime_checkable
class EmailSenderPort(Protocol):
    """
    Interface responsible for defining the contract for email sending.
    
    This port defines the contract that email sending adapters must implement.
    It allows the application layer to send emails without depending on
    specific email infrastructure implementations.
    """
    
    def send_email(self, email: EmailToSend) -> None:
        """
        Send an email.
        
        :param email: The email to send, containing header and content information.
        :type email: EmailToSend
        :return: None
        :rtype: None
        """
        ...

