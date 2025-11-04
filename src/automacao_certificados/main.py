from automacao_certificados.selenium_automations.websites.certidao_estadual_al.use_cases import get_certificado_using_groq
from automacao_certificados.selenium_automations.websites.certidao_municipal_maceio.use_cases import download_certificado
from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path

from automacao_certificados.selenium_automations.adapters.extractors import CertificadoMaceioExtractor

driver = WebDriver()
default_path = Path("/home/jgabrielsb/Downloads")

# extractor = CertificadoMaceioExtractor(
#     pdf_path=Path("certidao_maceio.pdf"),
# )

if __name__ == "__main__":
    download_certificado(
        driver=driver,
        cnpj="60604235000114",
        img_path_to_save=default_path,
    )

    #print(extractor.run())