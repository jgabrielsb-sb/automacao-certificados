
import pytest

from unittest.mock import MagicMock

from automacao_certificados.selenium_automations.core.exceptions import (
    LoggingRegisterException
)

from automacao_certificados.selenium_automations.core.interfaces import (
    LoggingRegisterPort
)

from automacao_certificados.selenium_automations.core.models import (
    LoggingRegisterInput
)

@pytest.fixture
def mock_logging_register():
    class MockLoggingRegister(LoggingRegisterPort):
        def register(self, input: LoggingRegisterInput):
            return None

    return MockLoggingRegister()


class TestLoggingRegisterPort:
    def test_if_run_raises_value_error_if_input_is_not_logging_register_input(
        self,
        mock_logging_register
    ):
        with pytest.raises(ValueError) as e:
            mock_logging_register.run('hello workd')
        
        assert 'LoggingRegisterInput' in str(e.value)

    def test_if_run_raises_logging_register_exception(
        self,
        monkeypatch,
        mock_logging_register
    ):
        def fake_register(self, input: LoggingRegisterInput):
            raise Exception('test exception')

        monkeypatch.setattr(mock_logging_register, "register", fake_register)

        with pytest.raises(LoggingRegisterException):
            mock_logging_register.run(MagicMock(spec=LoggingRegisterInput))
        


    

