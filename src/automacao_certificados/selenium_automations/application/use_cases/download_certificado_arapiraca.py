from automacao_certificados.selenium_automations.application.workflows import CertificadoArapiracaWorkflow
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_arapiraca.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters import *
from .exceptions import *

from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver



def _get_consulta_page(driver: WebDriver) -> ConsultaPage:
    return ConsultaPage(
        driver=driver,
    )

def _get_download_page(driver: WebDriver) -> DownloadPage:
    return DownloadPage(
        driver=driver,
    )

def download_certificado_arapiraca(
    cnpj: str,
) -> tuple[dto_document.DocumentExtracted, str]:
    driver = WebDriver()
    certificado_arapiraca_workflow = CertificadoArapiracaWorkflow(
        consulta_page=_get_consulta_page(driver=driver),
        download_page=_get_download_page(driver=driver),
    )
    try:
        return certificado_arapiraca_workflow.run(cnpj=cnpj)
    except Exception as e:
        raise DownloadCertificadoArapiracaException(
            original_exception=e
        )
    finally:
        driver.quit()
    