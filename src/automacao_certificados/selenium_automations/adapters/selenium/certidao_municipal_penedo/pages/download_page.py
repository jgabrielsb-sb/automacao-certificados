from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.interfaces.pages.download_page import DownloadInput
from automacao_certificados.selenium_automations.utils.utils import validate_document_file
from automacao_certificados.selenium_automations.adapters.extractors import CertificadoPenedoExtractor
from automacao_certificados.selenium_automations.core.models import dto_document

import base64
import os
import time
from pathlib import Path

from ..locators import locators


class DownloadPage(DownloadPagePort):
    """
    Page object model for the Download page for Penedo municipality.
    This page is used to download the certificate PDF file.
    """
    def __init__(
        self, 
        driver: WebDriver,
    ):
        self.driver = driver
        # Download directory is set in global_webdriver.py
        self.download_dir = Path(os.path.abspath("downloads"))

    def click_imprimir_button_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Imprimir button.
        To execute an executor the method 'run()' must be called.
        """
        imprimir_button_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.BTN_IMPRIMIR_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            imprimir_button_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def _count_pdf_files(self) -> int:
        """
        Count the number of PDF files in the download directory.
        Returns:
            The number of PDF files.
        """
        if not self.download_dir.exists():
            return 0
        
        pdf_files = list(self.download_dir.glob("*.pdf"))
        return len(pdf_files)

    def _wait_for_new_pdf_file(
        self,
        initial_count: int,
        timeout: int = 30
    ) -> Path:
        """
        Wait until a new PDF file appears in the download directory.
        Args:
            initial_count: The initial count of PDF files before clicking.
            timeout: Maximum time to wait in seconds.
        Returns:
            Path to the newly downloaded PDF file.
        Raises:
            TimeoutException: If no new PDF file is detected within timeout.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_count = self._count_pdf_files()
            
            if current_count > initial_count:
                # New file detected, get the most recently modified PDF file
                pdf_files = list(self.download_dir.glob("*.pdf"))
                if pdf_files:
                    # Sort by modification time, most recent first
                    pdf_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                    return pdf_files[0]
            
            time.sleep(0.5)  # Check every 500ms
        
        raise TimeoutException(
            f"No new PDF file detected in {timeout} seconds. "
            f"Initial count: {initial_count}, Current count: {self._count_pdf_files()}"
        )

    def get_certificado_base64_pdf(
        self
    ) -> str:
        """
        Get the certificado as base64 PDF string.
        This method clicks the imprimir button, waits for the PDF to download,
        and returns it as a base64 string.
        Returns:
            Base64-encoded PDF string.
        """
        # Count PDF files before clicking
        initial_pdf_count = self._count_pdf_files()
        
        # Click imprimir button
        self.click_imprimir_button_executor().run()
        
        # Wait for new PDF file to be downloaded
        pdf_path = self._wait_for_new_pdf_file(initial_pdf_count)
        
        # Read the PDF file and convert to base64
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        base64_str = base64.b64encode(pdf_bytes).decode("utf-8")
        
        # Validate the document
        validate_document_file(base64_str)
        
        return base64_str

    def run(
        self,
    ) -> tuple[dto_document.DocumentExtracted, str]:
        """
        Run the download page.
        Returns:
            Tuple containing (document_extracted, base64_pdf).
        """
        base64_pdf = self.get_certificado_base64_pdf()
        document_extracted = CertificadoPenedoExtractor(base64_pdf=base64_pdf).run()
        return document_extracted, base64_pdf
