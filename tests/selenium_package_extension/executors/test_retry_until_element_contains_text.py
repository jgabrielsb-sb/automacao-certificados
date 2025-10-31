import pytest
from unittest.mock import MagicMock, patch

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_package.interfaces.base_action import BaseAction

from automacao_certificados.selenium_package_extension.executors import RetryUntilElementContainsText

@pytest.fixture
def action_class() -> type[BaseAction]:
    """
    Fixture to create a BaseAction instance.
    """
    class MockAction(BaseAction):
        """
        Mock class for the BaseAction interface.
        """
        def __init__(
            self,
            driver: WebDriver,
        ):
            super().__init__(driver)

        def _execute_action(self) -> str:
            return "test"

    return MockAction


class TestRetryUntilElementContainsText:
    """
    Test class for the RetryUntilElementContainsText executor.
    """
    def test_if_raises_value_error_if_desired_text_is_not_a_string(
        self,
        action_class: type[BaseAction],
    ):
        """
        Test if the RetryUntilElementContainsText executor raises a ValueError if the desired text is not a string.
        """
        with pytest.raises(ValueError):
            RetryUntilElementContainsText(
                action=action_class(
                    driver=MagicMock(spec=WebDriver),
                ),
                web_element=MagicMock(spec=WebElement),
                desired_text=123,
            )

    def test_if_returns_true_if_the_element_has_the_desired_text(
        self,
        action_class: type[BaseAction],
    ):
        """
        Test if the RetryUntilElementContainsText executor returns True if the element contains the desired text.
        """
        mock_web_element = MagicMock(spec=WebElement)
        mock_web_element.text = "test"

        executor = RetryUntilElementContainsText(
            action=action_class(
                driver=MagicMock(spec=WebDriver),
            ),
            web_element=mock_web_element,
            desired_text="test",
        )

        assert executor._is_condition_to_stop_met() == True

    def test_if_returns_true_if_the_element_contains_the_desired_text(
        self,
        action_class: type[BaseAction],
    ):
        """
        Test if the RetryUntilElementContainsText executor returns True if the element contains the desired text.
        """
        mock_web_element = MagicMock(spec=WebElement)
        mock_web_element.text = "test and something else"

        executor = RetryUntilElementContainsText(
            action=action_class(
                driver=MagicMock(spec=WebDriver),
            ),
            web_element=mock_web_element,
            desired_text="test",
        )

        assert executor._is_condition_to_stop_met() == True

    def test_if_returns_false_if_the_element_does_not_contain_the_desired_text(
        self,
        action_class: type[BaseAction],
    ):
        """
        Test if the RetryUntilElementContainsText executor returns False if the element does not contain the desired text.
        """
        mock_web_element = MagicMock(spec=WebElement)
        mock_web_element.text = "something else"

        executor = RetryUntilElementContainsText(
            action=action_class(
                driver=MagicMock(spec=WebDriver),
            ),
            web_element=mock_web_element,
            desired_text="test",
        )

        assert executor._is_condition_to_stop_met() == False