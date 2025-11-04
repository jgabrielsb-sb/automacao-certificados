from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path
import time

from automacao_certificados.selenium_automations.websites.certidao_municipal_maceio.pages.consulta_page import ConsultaPage
from automacao_certificados.selenium_automations.adapters.extractors import CertificadoMaceioExtractor
def get_last_downloaded_pdf(
    download_dir: str | Path,
) -> Path | None:
    """
    Returns the most recently modified PDF file in the given directory.
    Ignores temporary/incomplete downloads.
    """
    download_dir = Path(download_dir)
    pdf_files = [
        f for f in download_dir.glob("*.pdf")
        if f.is_file() and not f.name.endswith(".crdownload")
    ]
    if not pdf_files:
        return None
    return max(pdf_files, key=lambda f: f.stat().st_mtime)

def download_certificado(
    driver: WebDriver,
    cnpj: str,
    img_path_to_save: Path,
) -> None:
    """
    Download the certificado of the company.
    """
    if not isinstance(driver, WebDriver):
        raise ValueError("driver must be a WebDriver object")
    if not isinstance(cnpj, str):
        raise ValueError("cnpj must be a string")
    if not isinstance(img_path_to_save, Path):
        raise ValueError("img_path_to_save must be a Path object")
    
    consulta_page = ConsultaPage(
        driver=driver,
        img_path_to_save=img_path_to_save,
    )
    consulta_page.run(cnpj=cnpj)
    last_downloaded_pdf = get_last_downloaded_pdf(download_dir=img_path_to_save)
    extractor = CertificadoMaceioExtractor(pdf_path=last_downloaded_pdf)
    print(extractor.run())

    #time.sleep(500)