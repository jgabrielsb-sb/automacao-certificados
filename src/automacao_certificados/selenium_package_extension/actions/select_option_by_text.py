from selenium_package.interfaces.base_action import BaseAction

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import Select

class SelectOptionByText(BaseAction):
    """
    Action that selects an option by text from a select element.
    """
    def __init__(
        self,
        driver: WebDriver,
        select_web_element: WebElement,
        desired_option_text: str,
    ):
        """
        Initializes the select option by text action.
        Args:
            driver: The web driver to use.
            select_web_element: The select element to select the option from.
            desired_option_text: The text of the option to select.
        Raises:
            ValueError: If desired_option_text is not a string.
        """
        if not select_web_element.tag_name == "select":
            raise ValueError("select_web_element must be a select element")

        if not isinstance(desired_option_text, str):
            raise ValueError("desired_option_text must be a string")
            
        super().__init__(
            driver,
            web_element=select_web_element, 
        )

        self.desired_option_text = desired_option_text

    def _execute_action(self) -> None:
        select_element = Select(self.web_element)
        select_element.select_by_visible_text(self.desired_option_text)
        