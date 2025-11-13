from automacao_certificados.selenium_automations.application.workflows import CertificadoMaceioWorkflow
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.config import settings
from .exceptions import *

from groq import Groq
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver


driver = WebDriver()

def _get_download_page(driver) -> DownloadPage:
    return DownloadPage(
        driver=driver,
    )

def download_certificado_maceio(
    cnpj: str,
) -> tuple[dto_document.DocumentExtracted, str]:
    driver = WebDriver()
    certificado_maceio_workflow = CertificadoMaceioWorkflow(
        download_page=_get_download_page(driver=driver),
    )
    try:
        return certificado_maceio_workflow.run(cnpj=cnpj)
    except Exception as e:
        raise DownloadCertificadoMaceioException(
            original_exception=e
        )
    finally:
        driver.quit()
    