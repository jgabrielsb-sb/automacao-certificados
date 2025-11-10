

from automacao_certificados.selenium_automations.adapters.captcha_gateway import SeleniumCaptchaGateway

import pytest

from unittest.mock import MagicMock

from selenium.webdriver.remote.webdriver import WebDriver

class TestInit:
    def test_if_raises_value_error_if_webdriver_is_not_a_webdriver(self):
        with pytest.raises(ValueError) as e:
            SeleniumCaptchaGateway(
                webdriver="not a webdriver",
                img_locator="img locator",
                input_locator="input locator",
            )

        assert "webdriver" in str(e.value)

    def test_if_raises_value_error_if_wait_for_is_not_int(self):
        with pytest.raises(ValueError) as e:
            SeleniumCaptchaGateway(
                webdriver=MagicMock(spec=WebDriver),
                img_locator="img locator",
                input_locator="input locator",
                wait_for="not an integer"
            )

        assert "wait_for" in str(e.value)

        