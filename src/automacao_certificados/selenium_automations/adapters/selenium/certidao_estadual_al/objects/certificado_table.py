from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_package.actions import *
from selenium_package.executors import *

from ..locators import locators

CNPJ_INDEX = 0
RAZAO_SOCIAL_INDEX = 1
UF_INDEX = 2

class CertificadoTable():
    """
    Object model for the Certificado table.
    This object model is used to get the certificado table.

    This table is composed by 3 columns: CNPJ, Razão Social and UF.
    Ideally, the table has only one row (I don´t know if it's possible to have more than one row).
    To acess the situation of the certificado, the method 'click_on_cnpj_executor()' must be called.
    """
    def __init__(
        self,
        driver: WebDriver,
        table_web_element: WebElement,
    ):
        if not isinstance(table_web_element, WebElement):
            raise ValueError("table_web_element must be a WebElement")

        if not isinstance(driver, WebDriver):
            raise ValueError("driver must be a WebDriver")

        self.driver = driver
        self.table_web_element = table_web_element

    def get_first_row_element(
        self,
    ) -> WebElement:
        """
        Get the first row of the table.
        """
        return WebDriverWait(self.table_web_element, 3).until(
            EC.presence_of_element_located(locators.ROW_LOCATOR)
        )
        

    def get_column_elements(
        self,
        row_element: WebElement,
    ) -> list[WebElement]:
        """
        Get the column elements of the row.
        Args:
            row_element: The row element to get the column elements from.
        Returns:
            A list of column elements.
        """
        return WebDriverWait(row_element, 3).until(
            EC.presence_of_all_elements_located(locators.COLUMNS_LOCATOR)
        )

    def get_cnpj_text(
        self,
    ) -> str:
        """
        Get the CNPJ text of the first row.
        Returns:
            The CNPJ text.
        """
        first_row_element = self.get_first_row_element()
        column_elements = self.get_column_elements(first_row_element)
        cnpj_element = column_elements[CNPJ_INDEX]
        return cnpj_element.text

    def get_razao_social_text(
        self,
    ) -> str:
        """
        Get the Razão Social text of the first row.
        Returns:
            The Razão Social text.
        """
        first_row_element = self.get_first_row_element()
        column_elements = self.get_column_elements(first_row_element)
        razao_social_element = column_elements[RAZAO_SOCIAL_INDEX]
        return razao_social_element.text

    def get_uf_text(
        self,
    ) -> str:
        """
        Get the UF text of the first row.
        Returns:
            The UF text.
        """
        first_row_element = self.get_first_row_element()
        column_elements = self.get_column_elements(first_row_element)
        uf_element = column_elements[UF_INDEX]
        return uf_element.text

    def click_on_cnpj_executor(
        self,
    ):
        """
        Click on the CNPJ of the first row.
        To execute an executor the method 'run()' must be called.
        Returns:
            The executor to click on the CNPJ.
        """
        first_row_element = self.get_first_row_element()
        column_elements = self.get_column_elements(first_row_element)
        cnpj_element = column_elements[CNPJ_INDEX]
        
        action = ClickOnElement(
            self.driver,
            cnpj_element,
        )

        executor = DefaultExecutor(
            action,
            cnpj_element,
        )

        return executor

 