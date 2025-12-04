from automacao_certificados.selenium_automations.application.use_cases.email_use_cases import SendApplicationBrokeReportViaEmailUseCase
from automacao_certificados.selenium_automations.composition.container import Container
from automacao_certificados.selenium_automations.core.models import (
    SendDownloadCertificatesReportViaEmailUseCaseInput,
    SendApplicationBrokeReportViaEmailUseCaseInput
)

from automacao_certificados.selenium_automations.core.exceptions.application.download_certificates_exceptions import DownloadCertificatesUseCaseException
from automacao_certificados.config import settings
from datetime import date
import time
import schedule

container = Container()
download_certificates_use_case = container.use_case_factory.create_download_certificates_use_case()
send_application_broke_email_use_case = container.use_case_factory.create_send_application_broke_report_via_email_use_case()
send_report_email_use_case = container.use_case_factory.create_send_download_certificates_report_via_email_use_case()

send_to_emails=["jgabrielsb2002@gmail.com"]
sender_email=settings.email_host_user

def run():
    download_certificates_output = download_certificates_use_case.run()
    send_report_email_use_case.run(
        input=SendDownloadCertificatesReportViaEmailUseCaseInput(
            download_certificates_output=download_certificates_output,
            send_to_emails=send_to_emails,
            sender_email=sender_email,
            date=date.today()
        )
    )


schedule.every().day.at(settings.run_cron_time).do(run)

RUN_WITH_CRON = settings.run_with_cron

if __name__ == "__main__":
    if RUN_WITH_CRON:
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    else:
        print('entrou')
        try:
            run()
        except DownloadCertificatesUseCaseException as e:
            send_application_broke_email_use_case.run(
                SendApplicationBrokeReportViaEmailUseCaseInput(
                    send_to_emails=send_to_emails,
                    sender_email=sender_email,
                    error_details=f"Razão do erro: {str(e)}"
                )
            )
            raise

            


        

