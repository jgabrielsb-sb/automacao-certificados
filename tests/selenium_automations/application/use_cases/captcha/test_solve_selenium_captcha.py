from unittest.mock import Mock, patch
import pytest

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from automacao_certificados.selenium_automations.application.use_cases.captcha.solve_selenium_captcha import solve_selenium_captcha
from automacao_certificados.selenium_automations.core.interfaces import BaseImageProcessor

class TestSolveSeleniumCaptcha:
    def test_if_raises_value_error_if_driver_is_not_a_web_driver(self):
        """
        Test if the solve_selenium_captcha raises a ValueError if the driver is not a WebDriver.
        """
        with pytest.raises(ValueError) as e:
            solve_selenium_captcha(
                driver="not_a_web_driver",
                adapter=Mock(spec=BaseImageProcessor),
                img_web_element=Mock(spec=WebElement),
                input_web_element=Mock(spec=WebElement),
            )

        assert "driver" in str(e.value)

    def test_if_raises_value_error_if_adapter_is_not_a_base_image_processor(self):
        """
        Test if the solve_selenium_captcha raises a ValueError if the adapter is not a BaseImageProcessor.
        """
        with pytest.raises(ValueError) as e:
            solve_selenium_captcha(
                driver=Mock(spec=WebDriver),
                adapter="not_a_base_image_processor",
                img_web_element=Mock(spec=WebElement),
                input_web_element=Mock(spec=WebElement),
            )

        assert "adapter" in str(e.value)

    def test_if_raises_value_error_if_img_web_element_is_not_a_web_element(self):
        """
        Test if the solve_selenium_captcha raises a ValueError if the img_web_element is not a WebElement.
        """
        with pytest.raises(ValueError) as e:
            solve_selenium_captcha(
                driver=Mock(spec=WebDriver),
                adapter=Mock(spec=BaseImageProcessor),
                img_web_element="not_a_web_element",
                input_web_element=Mock(spec=WebElement),
            )

        assert "img_web_element" in str(e.value)

    def test_if_raises_value_error_if_input_web_element_is_not_a_web_element(self):
        """
        Test if the solve_selenium_captcha raises a ValueError if the input_web_element is not a WebElement.
        """
        with pytest.raises(ValueError) as e:
            solve_selenium_captcha(
                driver=Mock(spec=WebDriver),
                adapter=Mock(spec=BaseImageProcessor),
                img_web_element=Mock(spec=WebElement),
                input_web_element="not_a_web_element",
            )

        assert "input_web_element" in str(e.value)

    def test_if_calls_correctly_the_captcha_page(self):
        """
        Test that solve_selenium_captcha instantiates CaptchaPage correctly
        and calls its solve_captcha() method.
        """
        mock_driver = Mock(spec=WebDriver)
        mock_adapter = Mock(spec=BaseImageProcessor)
        mock_img_web_element = Mock(spec=WebElement)
        mock_input_web_element = Mock(spec=WebElement)

        with patch(
            "automacao_certificados.selenium_automations.application.use_cases.captcha.solve_selenium_captcha.CaptchaPage"
        ) as mock_captcha_page:
            # Create a mock instance that will be returned when CaptchaPage(...) is called
            mock_instance = mock_captcha_page.return_value
            mock_instance.solve_captcha.return_value = "mocked_text"

            result = solve_selenium_captcha(
                driver=mock_driver,
                adapter=mock_adapter,
                img_web_element=mock_img_web_element,
                input_web_element=mock_input_web_element,
            )

            mock_captcha_page.assert_called_once_with(
                driver=mock_driver,
                img_web_element=mock_img_web_element,
                input_web_element=mock_input_web_element,
                image_processor=mock_adapter,
            )

            mock_instance.solve_captcha.assert_called_once()
            assert result == "mocked_text"