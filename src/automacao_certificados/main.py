from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver
from automacao_certificados.selenium_automations.application.use_cases import download_certificado_maceio

if __name__ == "__main__":
    driver = WebDriver()
    document_extracted, base64_pdf = download_certificado_maceio(
        cnpj="32652832000189",
    )
    print(f'document_extracted: {document_extracted} \n\n')
    print(f'base64_pdf: {base64_pdf} \n\n')
    driver.quit()