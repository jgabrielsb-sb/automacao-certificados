from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from automacao_certificados.selenium_automations.core.interfaces import (
    BasePage,
    BaseImageProcessor,
)
from automacao_certificados.selenium_automations.application.use_cases.captcha.solve_selenium_captcha import (
    solve_selenium_captcha, 
)

from selenium_package.interfaces import (
    BaseExecutor,
)
from selenium_package.actions import *
from selenium_package.executors import *

from ..locators import locators
from ..exceptions import *

from automacao_certificados.selenium_package_extension.actions import *
from automacao_certificados.selenium_package_extension.executors import *

URL = 'https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf'

from enum import Enum
from automacao_certificados.selenium_automations.core.models import StatesAcronym

class TipoInscricao(Enum):
    """
    Enum for the type of subscription.
    """
    CNPJ = "CNPJ"
    CEI = "CEI"
    
class ConsultaPage(BasePage):
    """
    Page object model for the Consulta page for the Caixa Econômica Federal.
    This page is used to search for a company in the Caixa Econômica Federal.
    The page is accessed through the following URL:
    https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf

    The page contains the following elements:
    - Input for the type of subscription (CNPJ or MEI)
    - Input for the value to be searched (CNPJ or MEI)
    - Input to select the state (UF)
    - Captcha image
    - Button to submit the form
    """
    def __init__(
        self, 
        driver: WebDriver,
        captcha_adapter: BaseImageProcessor,
    ):
        if not isinstance(captcha_adapter, BaseImageProcessor):
            raise ValueError("captcha_adapter must be a BaseImageProcessor")
        
        self.captcha_adapter = captcha_adapter
        super().__init__(driver)

    def redirect_to_page_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to redirect to the Consulta page.
        To execute an executor the method 'run()' must be called.
        """
        DESIRED_TAB_TITLE = "Consulta Regularidade"
        
        action = RedirectToPage(
            self.driver, 
            URL
        )

        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title=DESIRED_TAB_TITLE,
        )

        return executor

    def insert_tipo_inscricao_value_executor(
        self, 
        tipo_inscricao_value: str
    ) -> BaseExecutor:
        """
        Insert the type of subscription on the select input field.
        To execute an executor the method 'run()' must be called.
        Args:
            tipo_inscricao_value: the type as a string
        Raises:
            InvalidTipoInscricaoException: if the type value is invalid.
        """

        valid_types = [type.value for type in TipoInscricao]
        
        if tipo_inscricao_value not in valid_types:
            raise InvalidTipoInscricaoException(
                valid_tipo_inscricao_values=valid_types,
                tipo_inscricao_value=tipo_inscricao_value
            )

        select_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located(locators.SELECT_TIPO_INSCRICAO)
        )

        label_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.SELECT_TIPO_INSCRICAO_LABEL)
        )

        action = SelectOptionByText(
            self.driver,
            select_element,
            tipo_inscricao_value
        )

        executor = RetryUntilElementContainsText(
            action=action,
            web_element=label_element,
            desired_text=tipo_inscricao_value,
        )

        return executor

    def insert_captcha_value_executor(
        self, 
        captcha_value: str
    ) -> BaseExecutor:
        """
        Insert the captcha value on the captcha input field.
        To execute an executor the method 'run()' must be called.

        Args:
            captcha_value: the captcha value as a string
        """
        captcha_input_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CAPTCHA_INPUT_LOCATOR)
        )
        action = InsertText(
            self.driver,
            captcha_input_element,
            captcha_value
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=captcha_input_element,
            property_name="value",
            property_value=captcha_value,
        )

        return executor

    def insert_inscricao_value_executor(
        self, 
        inscricao_value: str
    ) -> BaseExecutor:
        """
        Insert the subscription value.
        To execute an executor the method 'run()' must be called.
        Args:
            inscricao_value: the value to be inserted
        """

        inscricao_input_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.INPUT_INSCRICAO)
        )
        action = InsertText(
            self.driver,
            inscricao_input_element,
            inscricao_value
        )

        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=inscricao_input_element,
            property_name="value",
            property_value=inscricao_value,
        )

        return executor

    def insert_estado_value_executor(
        self, 
        state_value: str
    ) -> BaseExecutor:
        """
        Insert the state on the state select field.
        To execute an executor the method 'run()' must be called.
        
        Args:
            state_value: the state value as a str
        Raises:
            InvalidEstadoException: if the state is invalid.
        """
        valid_states = [state.value for state in StatesAcronym]
        
        if state_value not in valid_states:
            raise InvalidEstadoException(
                valid_state_values=valid_states,
                state_value=state_value
            )
    
        select_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located(locators.SELECT_ESTADO)
        )
        
        label_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.SELECT_ESTADO_LABEL)
        )

        action = SelectOptionByValue(
            self.driver,
            select_element,
            state_value
        )

        executor = RetryUntilElementContainsText(
            action=action,
            web_element=label_element,
            desired_text=state_value,
        )

        return executor

    def click_consultar_button_executor(
        self
    ) -> BaseExecutor:
        """
        Click the consultar button.
        To execute an executor the method 'run()' must be called.
        """
        consultar_button_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CONSULTAR_BUTTON)
        )
        action = ClickOnElement(
            self.driver,
            consultar_button_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def solve_captcha(
        self
    ) -> None:
        """
        Solves the captcha by getting the captcha text from the image 
        and inserting it on the input field.
        """
        captcha_image_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CAPTCHA_IMAGE_LOCATOR)
        )
        captcha_input_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CAPTCHA_INPUT_LOCATOR)
        )
        
        captcha_text = solve_selenium_captcha(
            driver=self.driver,
            adapter=self.captcha_adapter,
            img_web_element=captcha_image_element,
            input_web_element=captcha_input_element,
        )

        return captcha_text


    def get_error_text(
        self
    ) -> str:
        """
        Get the error text.
        Returns:
            str: The error text.
            None: If the error text element is not found after 3 seconds.
        """
        from selenium.common.exceptions import TimeoutException

        try:
            error_text_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(locators.ERROR_TEXT)
            )
            return error_text_element.text
        except TimeoutException:
            return None

    def run(
        self,
        state_value: str,
        tipo_inscricao_value: str,
        inscricao_value: str,
        ) -> None:
        """
        Run the consulta page.
        To execute an executor the method 'run()' must be called.
        Args:
            state_value: the state value as a str
            tipo_inscricao_value: the type of subscription value as a str
            inscricao_value: the subscription value as a str
        """
        self.redirect_to_page_executor().run()
        self.insert_tipo_inscricao_value_executor(tipo_inscricao_value).run()
        
        captcha_text = self.solve_captcha()
        self.insert_inscricao_value_executor(inscricao_value).run()
        self.insert_estado_value_executor(state_value).run()
        self.click_consultar_button_executor().run()
        
        error_text = self.get_error_text()

        if error_text:
            INVALID_CAPTCHA_TEXT =  "Código Captcha Inválido"
            INCORRECT_CNPJ_TEXT = "Inscrição: informar o CNPJ correto"
            NOT_BASIC_CNPJ = "FGEN0946"
            NOT_FOUND_ON_UF = "Nao foi encontrado EMPREGADOR na UF"

            if INVALID_CAPTCHA_TEXT in error_text:
                raise InvalidCaptchaException(
                    captcha_value=captcha_text
                )
            if INCORRECT_CNPJ_TEXT in error_text:
                raise IncorrectCNPJException(
                    cnpj_value=inscricao_value
                )
            if NOT_BASIC_CNPJ in error_text:
                raise NotBasicCNPJException(
                    cnpj_value=inscricao_value
                )
            if NOT_FOUND_ON_UF in error_text:
                raise NotFoundOnUFException(
                    state_value=state_value,
                    cnpj_value=inscricao_value
                )
        
            




