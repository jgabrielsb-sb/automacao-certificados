from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.utils.utils import *
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
        with open("test.html", "w") as file:
            file.write(self.driver.page_source)
        # with open("test.pdf", "wb") as file:
        #     file.write(base64.b64decode(b64_pdf_str))
        validate_document_file(b64_pdf_str)
        return b64_pdf_str

    
