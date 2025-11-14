from selenium.webdriver.chrome.webdriver import WebDriver

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.utils.utils import *
from automacao_certificados.selenium_automations.adapters.extractors import CertidaoArapiracaExtractor
from ..locators import locators

class DownloadPage(DownloadPagePort):
    def __init__(
        self,
        driver: WebDriver,
    ):
        self.driver = driver

    def go_to_pdf_tab_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to go to the PDF tab.
        To execute an executor the method 'run()' must be called.
        """
        action = GoToTabThatHasTitle(
            self.driver,
            ""
        )
        executor = RetryActionUntilPageTitleIs(
            action=action,
            desired_page_title=""
        )
        return executor

    def run(
        self
    ) -> None:
        """
        Run the download page.
        To execute an executor the method 'run()' must be called.
        """
        import time
        self.go_to_pdf_tab_executor().run()
        b64_str_png = get_full_page_screenshot(self.driver)
        b64_pdf_str = png_base64_to_pdf_base64(b64_str_png)
        document_extracted = CertidaoArapiracaExtractor(
            html_content=self.driver.page_source
        ).run()
        validate_document_file(b64_pdf_str)
        return document_extracted, b64_pdf_str

    
