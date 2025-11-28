
from email.mime.multipart import MIMEMultipart
import pytest

from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailContent
from automacao_certificados.selenium_automations.infra.email.utils import (
    build_mime_multipart_email
)

from automacao_certificados.selenium_automations.core.models import (
    EmailToSend,
    EmailHeader
)

class TestBuildMimeMultiPartEmail:
    def test_if_raises_value_error_if_email_is_not_email_to_send_type(
        self
    ):
        with pytest.raises(ValueError) as e:
            build_mime_multipart_email("none")
        
        assert "email must be of type EmailToSend" in str(e.value)

    def test_if_returns_correct_email_object_when_is_html(
        self,
    ):
        email_to_send = EmailToSend(
            email_header=EmailHeader(
                recipient_email=["recipient@gmail.com"],
                sender_email="sender@gmail.com"
            ),
            email_content=EmailContent(
                subject='test',
                is_html=True,
                body='test'
            )
        )

        email_mime = build_mime_multipart_email(email_to_send)
        assert isinstance(email_mime, MIMEMultipart)
        assert email_mime["From"] == "sender@gmail.com"
        assert email_mime["To"] == "recipient@gmail.com"
        assert email_mime["Subject"] == "test"
        assert email_mime.get_payload()[0].get_content_type() == "text/html"
        assert email_mime.get_payload()[0].get_payload() == "test"
        
        
    def test_if_returns_correct_email_object_when_is_not_html(
        self,
    ):
        email_to_send = EmailToSend(
            email_header=EmailHeader(
                recipient_email=["recipient@gmail.com"],
                sender_email="sender@gmail.com"
            ),
            email_content=EmailContent(
                subject='test',
                is_html=False,
                body='test'
            )
        )

        email_mime = build_mime_multipart_email(email_to_send)
        assert isinstance(email_mime, MIMEMultipart)
        assert email_mime["From"] == "sender@gmail.com"
        assert email_mime["To"] == "recipient@gmail.com"
        assert email_mime["Subject"] == "test"
        assert email_mime.get_payload()[0].get_content_type() == "text/plain"
        assert email_mime.get_payload()[0].get_payload() == "test"
        
        
    def test_if_returns_correct_email_object_when_has_multiple_recipientes(
        self,
    ):
        email_to_send = EmailToSend(
            email_header=EmailHeader(
                recipient_email=["recipient1@gmail.com", "recipient2@gmail.com"],
                sender_email="sender@gmail.com"
            ),
            email_content=EmailContent(
                subject='test',
                is_html=True,
                body='test'
            )
        )
        email_mime = build_mime_multipart_email(email_to_send)
        assert isinstance(email_mime, MIMEMultipart)
        assert email_mime["From"] == "sender@gmail.com"
        assert email_mime["To"] == "recipient1@gmail.com, recipient2@gmail.com"
        assert email_mime["Subject"] == "test"
        assert email_mime.get_payload()[0].get_content_type() == "text/html"
        assert email_mime.get_payload()[0].get_payload() == "test"
        


    
