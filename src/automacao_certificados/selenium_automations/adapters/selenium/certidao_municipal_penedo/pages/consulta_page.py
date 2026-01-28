from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.utils.utils import validate_cnpj, format_cnpj
from automacao_certificados.selenium_automations.adapters.selenium.exceptions import IncorrectCNPJException
from automacao_certificados.selenium_automations.core.models.interfaces.dto_image_processor import (
    ImageProcessorInput,
)

import base64

from ..locators import locators

URL = 'https://gestor.tributosmunicipais.com.br/redesim/prefeitura/penedo/views/publico/portaldocontribuinte/publico/pessoajuridica/pessoajuridica.xhtml'


class ConsultaPage(ConsultaPagePort):
    """
    Page object model for the Consulta page for Penedo municipality.
    This page is used to search for a company certificate in Penedo.
    The page is accessed through the following URL:
    https://gestor.tributosmunicipais.com.br/redesim/prefeitura/penedo/views/publico/portaldocontribuinte/publico/pessoajuridica/pessoajuridica.xhtml

    The page flow:
    1. Navigate to initial page
    2. Click on "Certidão Negativa" button in menu
    3. Click on "Imobiliário" link
    4. Click on "Certidão Negativa" span
    5. Click CPF/CNPJ radio button
    6. Insert CNPJ
    7. Solve captcha
    8. Click "ENTRAR" button
    """
    def __init__(
        self, 
        driver: WebDriver,
        image_processor: ImageProcessorPort,
    ):
        self.driver = driver
        self.image_processor = image_processor

    def redirect_to_page_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to redirect to the Consulta page.
        To execute an executor the method 'run()' must be called.
        """
        DESIRED_PAGE_TITLE = "Portal do Contribuinte"
        
        action = RedirectToPage(
            self.driver, 
            URL
        )

        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title=DESIRED_PAGE_TITLE,
        )

        return executor

    def click_certidao_negativa_button_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Certidão Negativa button in the menu.
        To execute an executor the method 'run()' must be called.
        """
        btn_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.BTN_CERTIDAO_NEGATIVA_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            btn_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_imobiliario_link_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Imobiliário link.
        To execute an executor the method 'run()' must be called.
        """
        link_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.LINK_IMOBILIARIO_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            link_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_certidao_negativa_span_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Certidão Negativa span.
        To execute an executor the method 'run()' must be called.
        """
        span_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.SPAN_CERTIDAO_NEGATIVA_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            span_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_cpf_cnpj_radio_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the CPF/CNPJ radio button.
        To execute an executor the method 'run()' must be called.
        """
        radio_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.RADIO_CPF_CNPJ_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            radio_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def insert_cnpj_executor(
        self, 
        cnpj: str
    ) -> BaseExecutor:
        """
        Executor to insert the CNPJ.
        To execute an executor the method 'run()' must be called.
        Args:
            cnpj: the CNPJ value to be inserted
        """
        cnpj_input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locators.INPUT_CNPJ_LOCATOR)
        )
        
        action = InsertText(
            self.driver,
            cnpj_input_element,
            cnpj
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=cnpj_input_element,
            property_name="value",
            property_value=format_cnpj(cnpj),
        )

        return executor

    def solve_captcha_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to solve the captcha.
        To execute an executor the method 'run()' must be called.
        """
        if not isinstance(self.image_processor, ImageProcessorPort):
            raise ValueError("image_processor must be an ImageProcessorPort")
        
        # Get captcha image element
        captcha_image_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locators.IMAGE_CAPTCHA_LOCATOR)
        )
        
        # Solve captcha like test.ipynb:
        # - screenshot captcha image
        # - base64 encode
        # - use GroqImageProcessor (via ImageProcessorPort) to read the text
        png_bytes = captcha_image_element.screenshot_as_png
        captcha_b64 = base64.b64encode(png_bytes).decode("ascii")
        captcha_text = self.image_processor.get_text(
            ImageProcessorInput(base64_img=captcha_b64)
        ).text.strip()
        
        # Insert captcha text
        captcha_input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locators.INPUT_CAPTCHA_LOCATOR)
        )
        
        action = InsertText(
            self.driver,
            captcha_input_element,
            captcha_text
        )

        executor = RetryActionUntilElementHasAPropertyValue(
            action=action,
            web_element=captcha_input_element,
            property_name="value",
            property_value=captcha_text,
        )

        return executor

    def click_entrar_button_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Entrar button.
        To execute an executor the method 'run()' must be called.
        """
        entrar_button_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locators.BTN_ENTRAR_LOCATOR)
        )
        
        action = ClickOnElement(
            self.driver,
            entrar_button_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def is_error_present(
        self
    ) -> bool:
        """
        Check if there's an error message on the page.
        Returns True if error is present, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(locators.ERROR_MESSAGE_LOCATOR)
            )
            return True
        except TimeoutException:
            return False

    def run(
        self,
        cnpj: str,
    ) -> None:
        """
        Run the consulta page.
        Args:
            cnpj: the CNPJ value as a str
        """
        import time
        
        try:
            cnpj = validate_cnpj(cnpj)
        except Exception as e:
            raise IncorrectCNPJException(
                cnpj_value=cnpj
            )
        
        # Navigate to initial page
        self.redirect_to_page_executor().run()
        
        # Click on Certidão Negativa button
        self.click_certidao_negativa_button_executor().run()
        
        # Click on Imobiliário link
        self.click_imobiliario_link_executor().run()
        
        # Click on Certidão Negativa span
        self.click_certidao_negativa_span_executor().run()
        
        # Click CPF/CNPJ radio button
        self.click_cpf_cnpj_radio_executor().run()
        
        # Insert CNPJ
        self.insert_cnpj_executor(cnpj).run()
        
        # Solve captcha
        self.solve_captcha_executor().run()
        
        # Click Entrar button
        self.click_entrar_button_executor().run()
        
        # Small delay to ensure page is ready
        time.sleep(1)
        
        # Check for errors
        if self.is_error_present():
            raise IncorrectCNPJException(
                cnpj_value=cnpj
            )
