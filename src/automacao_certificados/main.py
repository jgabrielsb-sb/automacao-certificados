from automacao_certificados.selenium_automations.composition.container import Container
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.config import settings

import schedule
import time

container = Container()
download_certificates_use_case = container.use_case_factory.create_download_certificates_use_case()

def run():
    download_certificates_use_case.run()

schedule.every().day.at(settings.run_cron_time).do(run)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

