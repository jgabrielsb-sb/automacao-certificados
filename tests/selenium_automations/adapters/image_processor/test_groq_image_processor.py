import pytest

from unittest.mock import patch, MagicMock

from groq import Groq, NotFoundError

from automacao_certificados.selenium_automations.adapters import GroqImageProcessor
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

class TestGroqImageProcessor:
    """
    Test class for the GroqImageProcessor adapter.
    """
    def test_if_raises_value_error_if_client_is_not_a_groq_client(self):
        """
        Test if the GroqImageProcessor raises a ValueError if the client is not a Groq client.
        """
        with pytest.raises(ValueError):
            GroqImageProcessor(
                client=123,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )

    def test_if_raises_value_error_if_model_is_not_a_string(self):
        """
        Test if the GroqImageProcessor raises a ValueError if the model is not a string.
        """
        with pytest.raises(ValueError):
            GroqImageProcessor(
                client=Groq(api_key="KEY"),
                model=123,
            )   

    def test_if_raises_authentication_exception_if_api_key_is_invalid(self):
        from groq import AuthenticationError

        processor = GroqImageProcessor(
            client=Groq(api_key="invalid"),
        )

        with pytest.raises(AuthenticationException):
            from requests import Response
            with patch.object(
                processor.client.chat.completions, 
                'create', 
                side_effect=AuthenticationError(
                    message="Invalid API key",
                    response=Response(),
                    body='{"error":{"code":"invalid_api_key","message":"Invalid API key"}}',
                )
            ):
                processor.get_text(
                    input=ImageProcessorInput(base64_img="dhfjsdkfh")
                )

    def test_if_raises_invalid_parameters_exception_if_model_is_invalid(self):
        """
        Test if the GroqImageProcessor raises a InvalidParametersException if the model is invalid.
        """
        processor = GroqImageProcessor(
                client=Groq(api_key="KEY"),
                model="invalid",
            )
        
        with pytest.raises(InvalidParametersException) as exc_info:
            from groq import NotFoundError
            
            mock_response = MagicMock()
            mock_response.text = '{"error":{"code":"model_not_found","message":"Model not found"}}'

            with patch.object(
                processor.client.chat.completions, 
                'create', 
                side_effect=NotFoundError(
                    message="Model not found",
                    response=mock_response,
                    body='{"error":{"code":"model_not_found","message":"Model not found"}}',
                )
            ):
                processor.get_text(
                    input=ImageProcessorInput(base64_img="dhfjsdkfh")
                )
                    
        assert exc_info.value.service_name == "Groq"
        assert exc_info.value.parameter_name == "model"
        assert exc_info.value.parameter_value == "invalid"

        assert "Groq" in str(exc_info.value)
        assert "model" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test__get_text_success(self):
        # Arrange
        mock_groq = MagicMock(spec=Groq)
        mock_chat = MagicMock()
        mock_chat.choices = [MagicMock()]
        mock_chat.choices[0].message.content = "HELLO123"
        mock_groq.chat.completions.create.return_value = mock_chat

        processor = GroqImageProcessor(client=mock_groq)

        # Act
        result = processor.get_text(input=ImageProcessorInput(base64_img="fakebase64"))

        # Assert
        assert result.text == "HELLO123"
        mock_groq.chat.completions.create.assert_called_once()

            
