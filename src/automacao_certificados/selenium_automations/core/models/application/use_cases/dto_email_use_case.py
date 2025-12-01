from pydantic import BaseModel, EmailStr
from datetime import date
from automacao_certificados.selenium_automations.core.models.application.use_cases.dto_download_certificate_use_case import DownloadCertificatesUseCaseOutput

class SendEmailInput(BaseModel):
    send_to_emails: list[EmailStr]
    sender_email: EmailStr

class SendDownloadCertificatesReportViaEmailUseCaseInput(SendEmailInput):
    download_certificates_output: DownloadCertificatesUseCaseOutput
    date: date
    
class SendApplicationBrokeReportViaEmailUseCaseInput(SendEmailInput):
    error_details: str
