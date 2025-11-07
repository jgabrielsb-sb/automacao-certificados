from automacao_certificados.selenium_automations.application.services import captcha
from automacao_certificados.selenium_automations.application.services.captcha import (
    SolveCaptchaService, 
    SolveCaptchaOutput
)

import pytest

from unittest.mock import Mock

from automacao_certificados.selenium_automations.core.interfaces import (
    ImageProcessorPort,
    CaptchaGatewayPort,
)

class TestInit:
    def test_if_raises_value_error_if_image_processor_is_not_a_image_processor_port(self):
        """
        Test if the SolveCaptchaService raises a ValueError if the image_processor is not a ImageProcessorPort.
        """
        with pytest.raises(ValueError) as e:
            SolveCaptchaService(
                image_processor="not_a_image_processor_port",
                captcha_gateway=Mock(spec=CaptchaGatewayPort),
            )

        assert "image_processor" in str(e.value)

    def test_if_raises_value_error_if_captcha_gateway_is_not_a_captcha_gateway_port(self):
        """
        Test if the SolveCaptchaService raises a ValueError if the captcha_gateway is not a CaptchaGatewayPort.
        """
        with pytest.raises(ValueError) as e:
            SolveCaptchaService(
                image_processor=Mock(spec=ImageProcessorPort),
                captcha_gateway="not_a_captcha_gateway_port",
            )

        assert "captcha_gateway" in str(e.value)

class TestExecute:
    def test_sucess_case(
        self, 
        monkeypatch,
    ):
        def fake_get_captcha_base64_img():
            return "fake base64"

        def fake_fill_captcha_text(text):
            return SolveCaptchaOutput(
                retries=3,
                how_many_seconds=6
            )

        captcha_gateway = Mock(spec=CaptchaGatewayPort)
        monkeypatch.setattr(captcha_gateway, "get_captcha_base64_img", fake_get_captcha_base64_img)
        monkeypatch.setattr(captcha_gateway, "fill_captcha_text", fake_fill_captcha_text)


        def fake_get_text(base64_img):
            return "test"

        image_processor = Mock(spec=ImageProcessorPort)
        monkeypatch.setattr(image_processor, "get_text", fake_get_text)
        
        output = SolveCaptchaService(
            captcha_gateway=captcha_gateway,
            image_processor=image_processor
        ).execute()

        assert isinstance(output, SolveCaptchaOutput)
        assert output.retries == 3
        assert output.how_many_seconds == 6