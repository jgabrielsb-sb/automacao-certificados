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

def download_certidao_estadual_al(
    state_value: str,
    inscricao_value: str,
    img_path_to_save: Path,
) -> tuple[dto_document.DocumentExtracted, str]:

    consulta_page = ConsultaPage(
        driver=driver,
        captcha_solver=ImageCaptchaSolver(
            image_processor=GroqImageProcessor(client=groq),
            captcha_gateway=SeleniumCaptchaGateway(
                webdriver=driver,
            )
        )
    )

    download_page = DownloadPage(
        driver=driver,
    )

    certidao_estadual_al_workflow = CertidaoEstadualALWorkflow(
        consulta_page=consulta_page,
        download_page=download_page,
        img_path_to_save=img_path_to_save,
    )
    try:
        return certidao_estadual_al_workflow.run(
            state_value=state_value,
            tipo_inscricao_value="CNPJ",
            inscricao_value=inscricao_value,
        )
    except Exception as e:
        raise DownloadCertidaoEstadualAlException(original_exception=e)
    