# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

# from pathlib import Path

# from selenium_package.interfaces import *
# from selenium_package.actions import *
# from selenium_package.executors import *

# from automacao_certificados.selenium_package_extension.actions import *
# from automacao_certificados.selenium_automations.core.interfaces import BasePage
# from ..locators import locators
# from automacao_certificados.selenium_automations.utils.utils import format_cnpj
# import time
# URL = "https://siat.maceio.al.gov.br/dsf_mcz_portal/inicial.do?evento=montaMenu&acronym=EMITIRCERTIDAOFINANCEIRAPES"

# class ConsultaPage(BasePage):
#     """
#     Page object model for the Consulta page for the Certidao Municipal de Maceio.
#     This page is used to search for a company in the Certidao Municipal de Maceio.
#     The page is accessed through the following URL:
#     https://siat.maceio.al.gov.br/dsf_mcz_portal/inicial.do?evento=montaMenu&acronym=EMITIRCERTIDAOFINANCEIRAPES
#     """
#     def __init__(
#         self, 
#         driver: WebDriver,
#         img_path_to_save: Path,
#     ):
#         if not isinstance(img_path_to_save, Path):
#             raise ValueError("img_path_to_save must be a Path object")
        
#         super().__init__(driver)
#         self.img_path_to_save = img_path_to_save

#     def redirect_to_page_executor(
#         self
#     ) -> BaseExecutor:
#         """
#         Executor to redirect to the Consulta page.
#         To execute an executor the method 'run()' must be called.
#         """
#         action = RedirectToPage(
#             self.driver, 
#             URL
#         )
#         executor = RetryActionUntilPageTitleContains(
#             action=action,
#             desired_page_title="Prefeitura"
#         )
#         return executor

#     def insert_cnpj_executor(
#         self,
#         cnpj: str,
#     ) -> BaseExecutor:
#         """
#         Insert the CNPJ on the input field.
#         To execute an executor the method 'run()' must be called.
#         """
#         self.driver.switch_to.frame(0)

#         input_cnpj_element = WebDriverWait(self.driver, 3).until(
#             EC.presence_of_element_located(locators.INPUT_CNPJ_LOCATOR)
#         )
#         action = InsertText(
#             self.driver,
#             input_cnpj_element,
#             cnpj
#         )
#         executor = RetryActionUntilElementContainsAPropertyValue(
#             action=action,
#             web_element=input_cnpj_element,
#             property_name="value",
#             property_value=format_cnpj(cnpj),
#         )
#         return executor

#     def click_on_the_screen_executor(
#         self,
#     ) -> BaseExecutor:
#         """
#         Click on the screen.
#         To execute an executor the method 'run()' must be called.
#         """
#         action = ClickOnTheScreen(
#             self.driver,
#             x_coordinate=0,
#             y_coordinate=0,
#         )
#         executor = DefaultExecutor(
#             action=action
#         )
#         return executor

#     # def click_emitir_certificado_button_executor(
#     #     self,
#     # ) -> BaseExecutor:
#     #     """
#     #     Click the emitir certificado button.
#     #     To execute an executor the method 'run()' must be called.
#     #     """
#     #     emitir_certificado_button_element = WebDriverWait(self.driver, 10).until(
#     #         EC.element_to_be_clickable(locators.BTN_EMITIR_CERTIFICADO_LOCATOR)
#     #     )
            
#     #     action = ClickOnElement(
#     #         self.driver,
#     #         emitir_certificado_button_element
#     #     )
#     #     executor = RetryActionUntilNewFileHasBeenDetected(
#     #         action=action,
#     #         path=self.img_path_to_save,
#     #         file_extension=".pdf"
#     #     )
#     #     return executor

#     def run(
#         self,
#         cnpj: str,
#     ) -> None:
#         """
#         Run the Consulta page.
#         To execute an executor the method 'run()' must be called.
#         """
#         self.redirect_to_page_executor().run()
#         self.insert_cnpj_executor(cnpj=cnpj).run()
#         self.click_on_the_screen_executor().run()
#         #self.click_emitir_certificado_button_executor().run()