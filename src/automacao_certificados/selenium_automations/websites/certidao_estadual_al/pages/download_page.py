from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_package.executors import RetryActionUntilNewFileHasBeenDetected, RetryActionUntilPageTitleContains
from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import ClickOnElement

from pathlib import Path
import os

from automacao_certificados.selenium_automations.core.interfaces import BasePage
from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import *
from ..objects import CertificadoTable
from ..locators import locators

from automacao_certificados.selenium_package_extension.actions import TakeScreenshot


class DownloadPage(BasePage):
    """
    Page object model for the Download page for the Caixa Econômica Federal.
    This page is used to download the certificate of the company in the Caixa Econômica Federal.
    """
    def __init__(
        self, 
        driver: WebDriver,
    ):
        super().__init__(driver)

    def get_certificado_table_executor(
        self,
    ) -> CertificadoTable:
        """
        Get the CertificadoTable object.
        Returns:
            The CertificadoTable object.
        """
        table_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.TABLE_LOCATOR)
        )

        return CertificadoTable(
            driver=self.driver,
            table_web_element=table_element,
        )

    def click_on_cnpj_executor(
        self,
    ) -> BaseExecutor:
        """
        Click on the CNPJ of the CertificadoTable object.
        To execute an executor the method 'run()' must be called.
        Returns:
            The executor to click on the CNPJ.
        """
        executor = self.get_certificado_table_executor().click_on_cnpj_executor()
        return executor

    def click_on_certificado_href_executor(
        self,
    ) -> BaseExecutor:
        """
        Click on the Certificado href.
        To execute an executor the method 'run()' must be called.
        Returns:
            The executor to click on the Certificado href.
        """
        certificado_href_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CERTIFICADO_HREF_LOCATOR)
        )
        action = ClickOnElement(
            self.driver,
            certificado_href_element
        )
        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title="Certificado"
        )
        return executor

    def click_on_visualizar_button_executor(
        self,
    ) -> BaseExecutor:
        """
        Click on the Visualizar button.
        To execute an executor the method 'run()' must be called.
        Returns:
            The executor to click on the Visualizar button.
        """
        visualizar_button_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.VISUALIZAR_BUTTON_LOCATOR)
        )

        action = ClickOnElement(
            self.driver,
            visualizar_button_element
        )

        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title="Consulta"
        )

        return executor

    def get_certificado_image(
        self,
        img_path_to_save: Path,
    ) -> Path:
        """
        Get the certificado image.
        To execute an executor the method 'run()' must be called.
        Args:
            img_path_to_save: The path to save the image. Example: Path("certificado.png").
        Returns:
            The path to the saved image.
        """
        certificado_image_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CERTIFICADO_TABLE_LOCATOR)
        )
        action = TakeScreenshot(
            web_instance=self.driver,
            web_element=certificado_image_element,
            path_to_save=img_path_to_save
        )
        executor = RetryActionUntilNewFileHasBeenDetected(
            action=action,
            path=img_path_to_save.parent
        )
        return executor

    def _validate_img_path(
        self,
        img_path_to_save: Path,
    ) -> None:
        """
        Validate the img path.
        Args:
            img_path_to_save: The path to save the image. Example: Path("certificado.png").
        Raises:
            ImgPathAlreadyExistsException: If the file already exists.
            ImgPathException: If the file parent directory does not exist, is not a directory, or has insufficient permissions.
        """
        if not isinstance(img_path_to_save, Path):
            raise ValueError("img_path_to_save must be a Path object")
         
        # check if the file already exists
        if img_path_to_save.exists():
            raise ImgPathAlreadyExistsException(
                img_path=img_path_to_save
            )

        # check if the file parent directory exists
        if not img_path_to_save.parent.exists():
            raise ImgPathException(
                message=f"The file parent directory does not exist: {img_path_to_save.parent}"
            )

        # check if the file suffix is valid
        if not img_path_to_save.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            raise ImgPathException(
                message=f"The file suffix is not valid: {img_path_to_save.suffix}"
            )

        # check if has write permissions to save the file
        if not os.access(img_path_to_save.parent, os.W_OK):
            raise ImgPathException(
                message=f"Insufficient permissions to save the file: {img_path_to_save.parent}"
            )

    def _go_to_certificado_page(
        self,
    ) -> None:
        """
        Go to the certificado page.
        """
        self.click_on_cnpj_executor().run()
        self.click_on_certificado_href_executor().run()
        self.click_on_visualizar_button_executor().run()

    def _download_certificado(
        self,
        img_path_to_save: Path,
    ) -> None:
        """
        Download the certificado.
        Args:
            img_path_to_save: The path to save the image. Example: Path("certificado.png").
        """
        self.get_certificado_image(img_path_to_save=img_path_to_save).run()
    

    def run(
        self,
        img_path_to_save: Path,
    ) -> None:
        """
        Run the download page.
        Args:
            img_path_to_save: The path to save the image. Example: Path("certificado.png").
        Raises:
            ValueError: If the img path is not a Path object.
            ImgPathAlreadyExistsException: If the file already exists.
            ImgPathException: If the file parent directory does not exist, is not a directory, or has insufficient permissions.
        """
        self._validate_img_path(img_path_to_save=img_path_to_save)
        self.click_on_cnpj_executor().run()
        self.click_on_certificado_href_executor().run()
        self.click_on_visualizar_button_executor().run()
        self.get_certificado_image(img_path_to_save=img_path_to_save).run()