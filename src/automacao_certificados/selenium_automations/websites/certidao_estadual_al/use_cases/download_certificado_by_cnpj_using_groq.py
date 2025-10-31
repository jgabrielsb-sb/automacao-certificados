from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages import (
    ConsultaPage,
    DownloadPage,
)
from automacao_certificados.selenium_automations.adapters.image_processor import GroqImageProcessor
from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import *
from automacao_certificados.config import settings

def download_certificado_by_cnpj_using_groq(
    driver: WebDriver, 
    state_value: str,
    inscricao_value: str,
    img_path_to_save: Path
) -> None:
    """
    Download the certificado of the company by CNPJ using Groq.
    IMPORTANT: the CNPJ must be a basic CNPJ, that means that the CNPJ
    must have only the first 8 digits.
    Args:
        driver: The driver to use.
        state_value: The state value to use.
        inscricao_value: The CNPJ value to use.
    Raises:
        IncorrectCNPJException: If the CNPJ is incorrect.
        NotBasicCNPJException: If the CNPJ is not a basic CNPJ.
        NotFoundOnUFException: If the CNPJ is not found on the UF.
    """
    if not isinstance(driver, WebDriver):
        raise ValueError("driver must be a WebDriver object")
    if not isinstance(state_value, str):
        raise ValueError("state_value must be a string")
    if not isinstance(inscricao_value, str):
        raise ValueError("inscricao_value must be a string")
    if not isinstance(img_path_to_save, Path):
        raise ValueError("img_path_to_save must be a Path object")

    def _pass_consulta_page() -> None:
        """
        Pass the consulta page byL
        - Inserting CNPJ as subscription value
        - Inserting CNPJ
        """
        passed_consulta_page = False

        while not passed_consulta_page:
            try:
                ConsultaPage(
                    driver,
                    captcha_adapter=GroqImageProcessor(
                        groq_api_key=settings.groq_api_key,
                    ),
                ).run(
                    state_value=state_value,
                    tipo_inscricao_value="CNPJ",
                    inscricao_value=inscricao_value,
                )

                passed_consulta_page = True
            except InvalidCaptchaException:
                pass
            except (
                IncorrectCNPJException,
                NotBasicCNPJException,
                NotFoundOnUFException
            ):
                raise

    def _download_certificado() -> None:
        """
        Download the certificado of the company.
        """
        try:
            DownloadPage(
                driver=driver
            ).run(img_path_to_save=img_path_to_save)
        except DownloadPageException:
            raise
        
    _pass_consulta_page()
    _download_certificado()





    



