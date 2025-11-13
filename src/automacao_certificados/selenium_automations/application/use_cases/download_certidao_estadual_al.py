from automacao_certificados.selenium_automations.application.workflows import CertidaoEstadualALWorkflow
from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.config import settings
from .exceptions import *

from groq import Groq
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver


groq = Groq(api_key=settings.groq_api_key)
driver = WebDriver()

def _get_consulta_page() -> ConsultaPage:
    return ConsultaPage(
        driver=driver,
        captcha_solver=ImageCaptchaSolver(
            image_processor=GroqImageProcessor(client=groq),
            captcha_gateway=SeleniumCaptchaGateway(
                webdriver=driver,
            )
        )
    )

def _get_download_page() -> DownloadPage:
    return DownloadPage(
        driver=driver,
    )

def download_certidao_estadual_al(
    state_value: str,
    inscricao_value: str,
) -> tuple[dto_document.DocumentExtracted, str]:

    consulta_page = _get_consulta_page()
    download_page = _get_download_page()

    certidao_estadual_al_workflow = CertidaoEstadualALWorkflow(
        consulta_page=consulta_page,
        download_page=download_page,
    )
    try:
        return certidao_estadual_al_workflow.run(
            state_value=state_value,
            tipo_inscricao_value="CNPJ",
            inscricao_value=inscricao_value,
        )
    except Exception as e:
        raise DownloadCertidaoEstadualAlException(
            original_exception=e
        )
    finally:
        driver.quit()
    