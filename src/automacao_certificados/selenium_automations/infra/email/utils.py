from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailToSend

def build_mime_multipart_email(email: EmailToSend) -> MIMEMultipart:
    if not isinstance(email, EmailToSend):
        raise ValueError("email must be of type EmailToSend")
        
    email_object = MIMEMultipart()

    # updating body
    attach_mode = "html" if email.email_content.is_html else "plain"   
    email_object.attach(MIMEText(email.email_content.body, attach_mode))

    # updating header
    email_object["From"] = email.email_header.sender_email
    email_object["To"] = ", ".join(email.email_header.recipient_email)
    email_object["Subject"] = email.email_content.subject

    return email_object

