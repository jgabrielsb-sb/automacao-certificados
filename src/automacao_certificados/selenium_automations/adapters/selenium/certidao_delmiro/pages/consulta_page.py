from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from ..locators import locators
from ...exceptions import *

from automacao_certificados.selenium_package_extension.actions import *
from automacao_certificados.selenium_package_extension.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.interfaces.pages.consulta_page import ConsultaInput
from automacao_certificados.selenium_automations.utils.utils import format_cnpj

URL = 'https://agiliblue.agilicloud.com.br/portal/prefdelmirogouveia-al/#/certidao'

class ConsultaPage(ConsultaPagePort):
    """
    Page object model for the Consulta page for Delmiro Gouveia.
    This page is used to search for a company certificate in Delmiro Gouveia.
    The page is accessed through the following URL:
    https://agiliblue.agilicloud.com.br/portal/prefdelmirogouveia-al/#/certidao

    The page contains the following elements:
    - Select for the type of consultation (tipoConsulta)
    - Input for tipoConsultaEconomico
    - Input for CNPJ (cnpjCertidoes)
    - Select for the type of certificate (tipoCertidao)
    - Button to print certificate (btnImprimirCertidaoDebitos)
    - Radio button for new certificate (radNovaCertidao)
    - Button to continue (continuar button)
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
        Executor to redirect to the Consulta page.
        To execute an executor the method 'run()' must be called.
        """
        DESIRED_TAB_TITLE = "Portal"
        
        action = RedirectToPage(
            self.driver, 
            URL
        )

        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title=DESIRED_TAB_TITLE,
        )

        return executor

    def select_tipo_consulta_executor(
        self, 
        tipo_consulta_value: str = "Econômico"
    ) -> BaseExecutor:
        """
        Select the type of consultation on the select input field.
        To execute an executor the method 'run()' must be called.
        Args:
            tipo_consulta_value: the type as a string (default: "Econômico")
        """
        select_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located(locators.SELECT_TIPO_CONSULTA)
        )

        action = SelectOptionByText(
            self.driver,
            select_element,
            tipo_consulta_value
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_tipo_consulta_economico_executor(
        self
    ) -> BaseExecutor:
        """
        Click on the tipoConsultaEconomico input field.
        To execute an executor the method 'run()' must be called.
        """
        input_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locators.INPUT_TIPO_CONSULTA_ECONOMICO)
        )
        
        action = ClickOnElement(
            self.driver,
            input_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def insert_cnpj_executor(
        self, 
        cnpj_value: str
    ) -> BaseExecutor:
        """
        Insert the CNPJ value.
        To execute an executor the method 'run()' must be called.
        Args:
            cnpj_value: the CNPJ value to be inserted
        """
        cnpj_input_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locators.INPUT_CNPJ)
        )
        
        action = InsertText(
            self.driver,
            cnpj_input_element,
            cnpj_value
        )


        executor = RetryActionUntilElementContainsAPropertyValue(
            action=action,
            web_element=cnpj_input_element,
            property_name="value",
            property_value=format_cnpj(cnpj_value),
        )

        return executor

    def select_tipo_certidao_executor(
        self, 
        tipo_certidao_value: str = "Certidão de Débitos"
    ) -> BaseExecutor:
        """
        Select the type of certificate on the select input field.
        To execute an executor the method 'run()' must be called.
        Args:
            tipo_certidao_value: the type as a string (default: "Certidão de Débitos")
        """
        select_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located(locators.SELECT_TIPO_CERTIDAO)
        )

        action = SelectOptionByText(
            self.driver,
            select_element,
            tipo_certidao_value
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_imprimir_button_executor(
        self
    ) -> BaseExecutor:
        """
        Click the imprimir button.
        To execute an executor the method 'run()' must be called.
        """
        imprimir_button_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locators.BUTTON_IMPRIMIR)
        )
        
        action = ClickOnElement(
            self.driver,
            imprimir_button_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_radio_nova_certidao_executor(
        self
    ) -> BaseExecutor:
        """
        Click the radio button for new certificate.
        To execute an executor the method 'run()' must be called.
        """
        radio_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locators.RADIO_NOVA_CERTIDAO)
        )
        
        action = ClickOnElement(
            self.driver,
            radio_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def click_continuar_button_executor(
        self
    ) -> BaseExecutor:
        """
        Click the continuar button.
        To execute an executor the method 'run()' must be called.
        """
        continuar_button_element = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(locators.BUTTON_CONTINUAR)
        )
        
        action = ClickOnElement(
            self.driver,
            continuar_button_element
        )

        executor = DefaultExecutor(
            action=action
        )

        return executor

    def get_error_text(
        self
    ) -> str:
        """
        Get the error text.
        To execute an executor the method 'run()' must be called.
        """
        error_text_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.DIV_ERRO)
        )
        return error_text_element.text

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
        self.redirect_to_page_executor().run()
        self.select_tipo_consulta_executor().run()
        self.click_tipo_consulta_economico_executor().run()
        self.insert_cnpj_executor(cnpj).run()
        self.select_tipo_certidao_executor().run()
        self.click_imprimir_button_executor().run()
        self.click_radio_nova_certidao_executor().run()
        self.click_continuar_button_executor().run()
        time.sleep(2)

        error_text = self.get_error_text()
        if error_text == '':
            pass
        elif 'Não existe uma entidade' in error_text:
            raise CNPJNotFoundException(
                cnpj_value=cnpj
            )