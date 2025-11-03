from automacao_certificados.selenium_automations.websites.certidao_estadual_al.use_cases import get_certificado_using_groq
from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path
driver = WebDriver()

if __name__ == "__main__":
    get_certificado_using_groq(
        driver=driver,
        state_value="AL",
        inscricao_value="60604235",
        img_path_to_save=Path("src/automacao_certificados/data/certificados_caixa"),
    )