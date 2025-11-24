from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.config import settings

from datetime import datetime
import schedule
import time


use_case = DownloadCertificatesUseCase(
    ppe_api_requester=PPEAPIRequester(
        http=HttpxClient(),
        api_key=settings.ppe_api_key),
    workflow_selector=WorkflowSelector(
        municipio_api_requester=ReceitaAPIMunicipioGetter(
            api_requester=ReceitaAPIRequester(
                http=HttpxClient(),
            )
        )
    )
)

generator = DownloadCertificatesReportGenerator(
    save_path=Path("data/certificates_report"),
)

def run():
    certificates = use_case.run()
    file_path = generator.run(certificates, date=datetime.now())
    print(f"Report generated at {file_path}")

schedule.every().day.at(settings.run_cron_time).do(run)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)