
from automacao_certificados.selenium_automations.adapters.captcha_solver import ImageCaptchaSolver
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *

import pytest
from unittest.mock import MagicMock, Mock
from selenium.webdriver.remote.webelement import WebElement

class TestInit:
    def test_if_raises_value_error_if_image_processor_is_not_a_image_processor_port(self):
        """
        Test if the ImageCaptchaSolver raises a ValueError if the image_processor is not a ImageProcessorPort.
        """
        with pytest.raises(ValueError) as e:
            ImageCaptchaSolver(
                image_processor="not_a_image_processor_port",
                captcha_gateway=Mock(spec=SeleniumCaptchaGatewayPort),
            )

        assert "image_processor" in str(e.value)

    def test_if_raises_value_error_if_captcha_gateway_is_not_a_captcha_gateway_port(self):
        """
        Test if the ImageCaptchaSolver raises a ValueError if the captcha_gateway is not a SeleniumCaptchaGatewayPort.
        """
        with pytest.raises(ValueError) as e:
            ImageCaptchaSolver(
                image_processor=Mock(spec=ImageProcessorPort),
                captcha_gateway="not_a_captcha_gateway_port",
            )

        assert "captcha_gateway" in str(e.value)

class TestSolveCaptcha:
    def test_if_returns_the_captcha_text(
        self,
        monkeypatch
    ):
        image_processor = MagicMock(spec=ImageProcessorPort)
        image_processor._get_text.return_value = ImageProcessorOutput(text="test text")

        captcha_gateway = MagicMock(spec=SeleniumCaptchaGatewayPort)
        captcha_gateway.get_captcha_base64_img.return_value = "test img"
        captcha_gateway.fill_captcha_text.return_value = None
        
        output = ImageCaptchaSolver(
            image_processor,
            captcha_gateway
        )._solve_captcha(input=CaptchaSolverInput(
            input_webelement=MagicMock(spec=WebElement),
            img_webelement=MagicMock(spec=WebElement),
        ))

        assert output.text == "test text"