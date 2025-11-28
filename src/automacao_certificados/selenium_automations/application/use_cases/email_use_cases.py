from automacao_certificados.selenium_automations.core.interfaces import EmailSenderPort
from automacao_certificados.selenium_automations.core.models.application.use_cases import SendDownloadCertificatesReportViaEmailUseCaseInput
from automacao_certificados.selenium_automations.adapters.report_generator import DownloadCertificatesReportGenerator
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailToSend, EmailHeader, EmailContent

class SendDownloadCertificatesReportViaEmailUseCase:
    def __init__(self, email_sender: EmailSenderPort):
        if not isinstance(email_sender, EmailSenderPort):
            raise ValueError('email_sender must be EmailSenderPort')

        self.email_sender = email_sender
        self.download_certificates_report_generator = DownloadCertificatesReportGenerator()

    def run(self, input: SendDownloadCertificatesReportViaEmailUseCaseInput):
        download_certificates_report = self.download_certificates_report_generator.generate_report(input.download_certificates_output)

        self.email_sender.send_email(email=EmailToSend(
            email_header=EmailHeader(
                recipient_email=input.send_to_emails,
                sender_email=input.sender_email
            ),
            email_content=EmailContent(
                subject=f"Relatório de Certificados {input.date.strftime('%d/%m/%Y')}",
                is_html=True,
                body=download_certificates_report
            )
        ))