"""
Use case for solving a captcha.
The contract of the use case is:

def solve_selenium_captcha(
    driver: WebDriver,
    adapter: BaseImageProcessor,
    img_web_element: WebElement,
    input_web_element: WebElement,
) -> None:
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from automacao_certificados.selenium_automations.adapters.ui.selenium.pages import CaptchaPage

from automacao_certificados.selenium_automations.core.interfaces import BaseImageProcessor
        
def solve_selenium_captcha(
    driver: WebDriver,
    adapter: BaseImageProcessor,
    img_web_element: WebElement,
    input_web_element: WebElement,
) -> None:
    """
    Solves a captcha that is displayed on a selenium page.
    Args:
        driver: The driver to use to interact with the page.
        adapter: The image processing adapter that will be used to get the 
        captcha text from the image displayed on the page.
        img_web_element: The web element that contains the captcha image.   
        input_web_element: The web element that contains the input field.
    """
    def _validate_parameters(
        driver: WebDriver,
        adapter: BaseImageProcessor,
        img_web_element: WebElement,
        input_web_element: WebElement,
    ) -> None:
        """
        Validates the parameters for the solve_selenium_captcha use case.
        """
        if not isinstance(driver, WebDriver):
            raise ValueError("webdriver must be a WebDriver")

        if not isinstance(adapter, BaseImageProcessor):
            raise ValueError("adapter must be a BaseImageProcessor")
        
        if not isinstance(img_web_element, WebElement):
            raise ValueError("img_web_element must be a WebElement")
        
        if not isinstance(input_web_element, WebElement):
            raise ValueError("input_web_element must be a WebElement")
        

    _validate_parameters(driver, adapter, img_web_element, input_web_element)

    page = CaptchaPage(
        driver=driver,
        img_web_element=img_web_element,
        input_web_element=input_web_element,
        image_processor=adapter,
    )

    captcha_text = page.solve_captcha()
    return captcha_text

        






        


    
