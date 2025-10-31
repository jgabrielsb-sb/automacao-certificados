from selenium_package.interfaces.base_action import BaseAction

from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class TakeScreenshot(BaseAction):
    """
    Action that takes a screenshot of a web page or 
    a web element and saves the imagegiven a path to 
    save it.
    You can take a screenshot of a web page or a web element.
    If you want to take a screenshot of a web page, you must pass None to the web_element parameter.
    If you want to take a screenshot of a web element, you must pass the web element to the web_element parameter.
    """
    def __init__(
        self,
        web_instance: WebDriver,
        web_element: WebElement | None = None,
        path_to_save: Path = Path("screenshot.png"),
    ):
        """
        Initializes the take screenshot action.
        Args:
            web_instance: The web Driver to use.
            web_element: The web element to take the screenshot from.
            path_to_save: The path to save the screenshot.
        Raises:
            ValueError: If desired_option_value is not a string.
        """
        if not isinstance(web_instance, WebDriver):
            raise ValueError("web_instance must be a WebDriver")

        if not isinstance(path_to_save, Path):
            raise ValueError("path_to_save must be a Path")

        if path_to_save.suffix != ".png":
            raise ValueError("path_to_save must end with .png")

        if web_element is not None and not isinstance(web_element, WebElement):
            raise ValueError("web_element must be a WebElement")
            
        super().__init__(web_instance, web_element=web_element)
        self.path_to_save = path_to_save

    def _execute_action(self) -> None:
        print(f"Taking screenshot of {self.path_to_save}")
        try:
            if self.web_element is not None:
                print(f"Taking screenshot of web element {self.web_element}")
                self.web_element.screenshot(str(self.path_to_save))
            else:
                print(f"Taking screenshot of web instance {self.web_instance}")
                self.web_instance.save_screenshot(str(self.path_to_save))
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            raise e