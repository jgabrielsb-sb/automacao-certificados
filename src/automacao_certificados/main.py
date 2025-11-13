from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver

if __name__ == "__main__":
    driver = WebDriver()
    consulta_page = ConsultaPage(
        driver=driver,
        img_path_to_save=Path("certificado.png"),
    )
    consulta_page.run(cnpj="60604235")