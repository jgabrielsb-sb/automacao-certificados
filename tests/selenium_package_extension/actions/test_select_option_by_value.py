import pytest
from unittest.mock import MagicMock, patch

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from automacao_certificados.selenium_package_extension.actions import SelectOptionByValue


class TestSelectOptionByValue:
    """
    Test class for the SelectOptionByValue action.
    """
    def test_if_raises_value_error_if_desired_option_value_is_not_a_string(
        self,
    ):
        """
        Test if the SelectOptionByText action raises a ValueError if the desired option text is not a string.
        """

        with pytest.raises(ValueError):
            SelectOptionByValue(
                driver=MagicMock(spec=WebDriver),
                select_web_element=MagicMock(spec=WebElement),
                desired_option_value=123,
            )

    def test_if_raises_value_error_if_select_web_element_is_not_a_select_element(
        self,
    ):
        """
        Test if the SelectOptionByText action raises a ValueError if the select web element is not a select element.
        """
        mock_web_element = MagicMock(spec=WebElement)
        mock_web_element.tag_name = "div"

        with pytest.raises(ValueError) as e:
            SelectOptionByValue(
                driver=MagicMock(spec=WebDriver),
                select_web_element=mock_web_element,
                desired_option_value="test",
            )

        assert "select_web_element" in str(e.value)

    def test_if_calls_correct_methods(
        self,
    ):
        from selenium.webdriver.support.ui import Select
        
        mock_select_web_element = MagicMock(spec=WebElement)
        mock_select_web_element.tag_name = "select"

        with patch.object(
            Select, 
            "select_by_value"
        ) as mock_select_by_visible_text:
            action = SelectOptionByValue(
                driver=MagicMock(spec=WebDriver),
                select_web_element=mock_select_web_element,
                desired_option_value="test",
            )
            action.execute_action()

            mock_select_by_visible_text.assert_called_once_with("test")
