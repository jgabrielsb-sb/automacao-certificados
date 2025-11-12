

from automacao_certificados.selenium_automations.adapters.captcha_gateway import SeleniumCaptchaGateway

import pytest

from unittest.mock import MagicMock

from selenium.webdriver.remote.webdriver import WebDriver

class TestInit:
    def test_if_raises_value_error_if_webdriver_is_not_a_webdriver(self):
        with pytest.raises(ValueError) as e:
            SeleniumCaptchaGateway(
                webdriver="not a webdriver",
            )

        assert "webdriver" in str(e.value)


        