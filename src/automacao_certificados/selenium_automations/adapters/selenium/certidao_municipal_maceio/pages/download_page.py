from selenium.webdriver.chrome.webdriver import WebDriver

from selenium_package.executors import *
from selenium_package.interfaces import *
from selenium_package.actions import *

import requests
from pathlib import Path
import base64

from automacao_certificados.selenium_automations.adapters.extractors import CertificadoMaceioExtractor
from automacao_certificados.selenium_automations.adapters.selenium.exceptions import SeleniumAdapterException
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import dto_document
from automacao_certificados.selenium_automations.utils.utils import *


URL = "https://siat.maceio.al.gov.br/dsf_mcz_portal/inicial.do?evento=montaMenu&acronym=EMITIRCERTIDAOFINANCEIRAPES"

class DownloadPage(DownloadPagePort):
    """
    Page object model for the Download page for the Caixa Econômica Federal.
    This page is used to download the certificate of the company in the Caixa Econômica Federal.
    """
    def __init__(
        self, 
        driver: WebDriver,
    ):
        self.driver = driver

    def redirect_to_page_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to redirect to the Download page.
        To execute an executor the method 'run()' must be called.
        """
        action = RedirectToPage(
            self.driver, URL)
        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title="Prefeitura"
        )
        return executor

    def get_certificado_base64_pdf(
        self,
        cnpj: str,
    ) -> str:

        def _build_session_from_selenium() -> requests.Session:
            session = requests.Session()
            for cookie in self.driver.get_cookies():
                session.cookies.set(cookie['name'], cookie['value'])
            return session
        
        session = _build_session_from_selenium()
        response = session.post(
            url="https://siat.maceio.al.gov.br/dsf_mcz_gtm/por/emitircertidaofinanceiracon.do?evento=Emitir%20Certid%E3o",
            data={
                'cadastroCodigoPesquisa': format_cnpj(cnpj),
                'cadastroTipoCadastro': 'P'
            }
        )
        bytes = response.content
        base64_str = base64.b64encode(bytes).decode("utf-8")
        validate_document_file(base64_str)
        return base64_str


    def run(
        self,
        cnpj: str,
    ) -> tuple[dto_document.DocumentExtracted, str]:
        """
        Run the download page.
        Args:
            cnpj: The CNPJ of the company.
        """
        cnpj = validate_cnpj(cnpj)
        self.redirect_to_page_executor().run() 
        base64_pdf = self.get_certificado_base64_pdf(cnpj=cnpj)
        document_extracted = CertificadoMaceioExtractor(base64_pdf=base64_pdf).run()
        return document_extracted, base64_pdf