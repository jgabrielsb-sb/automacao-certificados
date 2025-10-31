from selenium_package.interfaces.base_action import BaseAction

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import Select

class SelectOptionByValue(BaseAction):
    """
    Action that selects an option by value from a select element.
    """
    def __init__(
        self,
        driver: WebDriver,
        select_web_element: WebElement,
        desired_option_value: str,
    ):
        """
        Initializes the select option by value action.
        Args:
            driver: The web driver to use.
            select_web_element: The select element to select the option from.
            desired_option_value: The value of the option to select.
        Raises:
            ValueError: If desired_option_value is not a string.
        """
        if not select_web_element.tag_name == "select":
            raise ValueError("select_web_element must be a select element")

        if not isinstance(desired_option_value, str):
            raise ValueError("desired_option_value must be a string")
            
        super().__init__(
            driver,
            web_element=select_web_element,
        )

        self.desired_option_value = desired_option_value

    def _execute_action(self) -> None:
        select_element = Select(self.web_element)
        select_element.select_by_value(self.desired_option_value)
        