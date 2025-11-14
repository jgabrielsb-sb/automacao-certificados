
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver

from selenium_package.interfaces import BaseExecutor
from selenium_package.actions import *
from selenium_package.executors import *

from automacao_certificados.selenium_automations.core.interfaces import *
from ..locators import locators

URL = 'https://arapiraca.abaco.com.br/eagata/portal/'

class ConsultaPage(ConsultaPagePort):
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
        DESIRED_PAGE_TITLE = "Contribuinte"
        action = RedirectToPage(
            self.driver, 
            URL
        )
        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title=DESIRED_PAGE_TITLE,
        )
        return executor

    def click_certidao_geral_button_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Certidão Geral button.
        To execute an executor the method 'run()' must be called.
        """
        btn_certidao_geral_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.BTN_CERTIDAO_GERAL_LOCATOR)
        )
        action = ClickOnElement(
            self.driver, 
            btn_certidao_geral_element
        )
        executor = RetryActionUntilAnotherTabIsOpened(
            action=action,
            current_tabs_count=1,
        )
        return executor

    def go_to_certidao_tab_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to go to the Certidão tab.
        To execute an executor the method 'run()' must be called.
        """
        action = GoToTabThatContainsTitle(
            self.driver, 
            "Emissão"
        )
        executor = RetryActionUntilPageTitleContains(
            action=action,
            desired_page_title="Emissão",
        )
        return executor

    def select_pessoa_juridica(
        self
    ) -> BaseExecutor:
        """
        Executor to select the Pessoa Jurídica option.
        To execute an executor the method 'run()' must be called.
        """
        from selenium.webdriver.support.ui import Select
        
        select_pessoa_juridica_element = Select(
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(locators.SELECT_PESSOA_JURIDICA_LOCATOR)
            )
        )

        select_pessoa_juridica_element.select_by_visible_text("Pessoa Jurídica")

    def insert_cnpj_executor(
        self,
        cnpj: str
    ) -> BaseExecutor:
        """
        Executor to insert the CNPJ.
        To execute an executor the method 'run()' must be called.
        """
        cnpj_input_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.INPUT_CNPJ_LOCATOR)
        )

        action = InsertText(
            self.driver,
            cnpj_input_element,
            cnpj
        )

        executor = RetryActionUntilElementHasAPropertyValue(
            action=action,
            web_element=cnpj_input_element,
            property_name="value",
            property_value=cnpj,
        )

        return executor

    def click_consultar_button_executor(
        self
    ) -> BaseExecutor:
        """
        Executor to click the Consultar button.
        To execute an executor the method 'run()' must be called.
        """
        consultar_button_element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located(locators.CONSULTAR_BUTTON_LOCATOR)
        )
        action = ClickOnElement(
            self.driver,
            consultar_button_element
        )
        executor = RetryActionUntilAnotherTabIsOpened(
            action=action,
            current_tabs_count=2,
        )
        return executor


    def run(
        self,
        cnpj: str
    ) -> None:
        """
        Run the consulta page.
        To execute an executor the method 'run()' must be called.
        """
        import time
        self.redirect_to_page_executor().run()
        self.click_certidao_geral_button_executor().run()
        self.go_to_certidao_tab_executor().run()
        self.select_pessoa_juridica()
        time.sleep(2)
        self.insert_cnpj_executor(cnpj).run()
        self.click_consultar_button_executor().run()