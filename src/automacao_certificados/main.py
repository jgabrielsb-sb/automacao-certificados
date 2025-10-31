from selenium.webdriver.chrome.webdriver import WebDriver

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages import ConsultaPage
from automacao_certificados.selenium_automations.adapters.image_processor.groq_image_processor import GroqImageProcessor

from automacao_certificados.config import settings

from pathlib import Path
import time

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.use_cases import download_certificado_by_cnpj_using_groq


if __name__ == "__main__":
    driver = WebDriver()
    CNPJ = "60604235"

    download_certificado_by_cnpj_using_groq(
        driver=driver,
        state_value="AL",
        captcha_adapter=GroqImageProcessor(
            groq_api_key=settings.groq_api_key,
        ),
        inscricao_value=CNPJ,
        img_path_to_save=Path("/home/jgabrielsb/Documents/Programming/Sebrae/automacao-certificados/src/automacao_certificados/data/certificados/certificado.png"),
    )

    time.sleep(1000)

   
