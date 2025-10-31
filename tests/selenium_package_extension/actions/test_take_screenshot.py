import pytest
from unittest.mock import MagicMock, patch

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pathlib import Path

from automacao_certificados.selenium_package_extension.actions import TakeScreenshot

class TestTakeScreenshot:
    """
    Test class for the TakeScreenshot action.
    """
    def test_if_raises_value_error_if_driver_is_not_a_web_driver(self):
        """
        Test if the TakeScreenshot action raises a ValueError if the driver is not a WebDriver.
        """
        with pytest.raises(ValueError) as e:
            TakeScreenshot(
                web_instance="not_a_web_driver", 
                web_element=None, 
                path_to_save=Path("screenshot.png")
            )

        assert "web_instance" in str(e.value)

    def test_if_raises_value_error_if_web_element_is_not_a_web_element(self):
        """
        Test if the TakeScreenshot action raises a ValueError if the web element is not a WebElement.
        """
        with pytest.raises(ValueError) as e:
            TakeScreenshot(
                web_instance=MagicMock(spec=WebDriver),
                web_element="not_a_web_element",
                path_to_save=Path("screenshot.png")
            )

        assert "web_element" in str(e.value)

    def test_if_raises_value_error_if_path_to_save_is_not_a_path(self):
        """
        Test if the TakeScreenshot action raises a ValueError if the path to save is not a Path.
        """
        with pytest.raises(ValueError) as e:
            TakeScreenshot(
                web_instance=MagicMock(spec=WebDriver),
                web_element=None,
                path_to_save="not_a_path"
            )

        assert "path_to_save" in str(e.value)

    def test_if_raises_value_error_if_path_to_save_does_not_end_with_png(self):
        """
        Test if the TakeScreenshot action raises a ValueError if the path to save does not end with .png.
        """
        with pytest.raises(ValueError) as e:
            TakeScreenshot(
                web_instance=MagicMock(spec=WebDriver),
                web_element=None,
                path_to_save=Path("screenshot.pdf")
            )

        assert "path_to_save" in str(e.value)

    def test_if_calls_driver_save_screenshot_if_web_element_is_none(self):
        """
        Test if the TakeScreenshot action calls the driver save_screenshot method if the web element is None.
        """
        driver = MagicMock(spec=WebDriver)
        action = TakeScreenshot(
            web_instance=driver,
            web_element=None,
            path_to_save=Path("screenshot.png")
        )
        with patch.object(driver, "save_screenshot") as mock_save_screenshot:
            action._execute_action()
            mock_save_screenshot.assert_called_once_with(str(Path("screenshot.png")))

    def test_if_calls_web_element_screenshot_if_web_element_is_not_none(self):
        """
        Test if the TakeScreenshot action calls the web element screenshot method if the web element is not None.
        """
        driver = MagicMock(spec=WebDriver)
        web_element = MagicMock(spec=WebElement)
        
        action = TakeScreenshot(
            web_instance=driver,
            web_element=web_element,
            path_to_save=Path("screenshot.png")
        )
        
        with patch.object(web_element, "screenshot") as mock_screenshot:
            action._execute_action()
            mock_screenshot.assert_called_once_with(str(Path("screenshot.png")))