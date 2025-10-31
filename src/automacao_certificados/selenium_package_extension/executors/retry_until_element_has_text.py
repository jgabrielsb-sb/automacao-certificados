from selenium_package.interfaces import *
from selenium.webdriver.remote.webelement import WebElement

class RetryUntilElementHasText(BaseExecutor):
    """
    Executor that retries an action until an element has a specific text.
    """
    def __init__(
        self,
        action: BaseAction,
        web_element: WebElement,
        desired_text: str,
    ):
        """
        Initializes the retry until element has text executor.
        Args:
            action: The action to be executed and retried.
            web_element: The web element to check the text of.
            desired_text: The text to check if the element has.
        Raises:
            ValueError: If desired_text is not a string.
        """
        super().__init__(
            action=action,
            web_element=web_element,
        )

        if not isinstance(desired_text, str):
            raise ValueError("desired_text must be a string")

        self.desired_text = desired_text

    def _is_condition_to_stop_met(self) -> bool:
        if self.web_element.text == self.desired_text:
            return True
        
        return False