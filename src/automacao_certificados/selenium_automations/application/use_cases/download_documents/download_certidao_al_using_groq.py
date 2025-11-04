from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages import (
    ConsultaPage,
    DownloadPage,
)
from automacao_certificados.selenium_automations.adapters.image_processor import GroqImageProcessor
from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import *
from automacao_certificados.config import settings

from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.adapters.extractors.certificado_caixa_extractor import CertificadoCaixaExtractor

from automacao_certificados.selenium_automations.application.services.api import CertificadoAPIService
from automacao_certificados.selenium_automations.adapters.api_requester import CertificadoAPIRequester

def get_certificado_using_groq(
    driver: WebDriver, 
    state_value: str,
    inscricao_value: str,
    img_path_to_save: Path,
) -> tuple[dto_document.DocumentExtracted, Path]:
    """
    Download the certificado of the company by CNPJ using Groq.
    IMPORTANT: the CNPJ must be a basic CNPJ, that means that the CNPJ
    must have only the first 8 digits.
    Args:
        driver: The driver to use.
        state_value: The state value to use.
        inscricao_value: The CNPJ value to use.
        img_path_to_save: The path to save the image.
    Returns:
        The certificado extracted and the path to save the image.
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

    def _go_to_certificado_page() -> None:
        """
        Go to the certificado page.
        """
        DownloadPage(
            driver=driver
        )._go_to_certificado_page()

    def _download_certificado(
        img_path_to_save: Path,
    ) -> None:
        """
        Download the certificado of the company.
        Args:
            img_path_to_save: The path to save the image. Example: Path("certificado.png").
        """
        DownloadPage(driver=driver)._download_certificado(img_path_to_save=img_path_to_save)

    def _get_certificado():
        """
        Get the certificado of the company.
        """
        certificado_extractor = CertificadoCaixaExtractor(driver=driver)
        certificado = certificado_extractor.run()
        return certificado
    
    def _get_path_to_save(
        certificado: dto_document.DocumentExtracted,
    ) -> Path:
        """
        Get the path to save the certificado.
        """
        cnpj = certificado.supplier.cnpj.replace('.', '').replace('/', '').replace('-', '')
        expiration_date = certificado.expiration_date.strftime("%d%m%Y")
        return Path("src/automacao_certificados/data/certificados_caixa") / f"{cnpj}_{expiration_date}.png"
        
    _pass_consulta_page()
    _go_to_certificado_page()
    certificado = _get_certificado()
    
    img_path_to_save = _get_path_to_save(certificado=certificado)
    _download_certificado(img_path_to_save)

    certificado_api_service = CertificadoAPIService(
        api_requester=CertificadoAPIRequester(
            base_url=settings.base_certificado_api_url
        )
    )
    document = certificado_api_service.register_document(document=certificado)

    return document





    



