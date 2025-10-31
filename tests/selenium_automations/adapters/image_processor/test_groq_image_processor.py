import pytest
from unittest.mock import patch, MagicMock

from automacao_certificados.selenium_automations.adapters import GroqImageProcessor
from automacao_certificados.selenium_automations.adapters.image_processor.exceptions import (
    AuthenticationException,
    InvalidParametersException,
    UnexpectedImageProcessingException,
)

from groq import ( 
    NotFoundError
)

class TestGroqImageProcessor:
    """
    Test class for the GroqImageProcessor adapter.
    """
    def test_if_raises_value_error_if_groq_api_key_is_not_a_string(self):
        """
        Test if the GroqImageProcessor raises a ValueError if the groq_api_key is not a string.
        """
        with pytest.raises(ValueError):
            GroqImageProcessor(
                groq_api_key=123,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )

    def test_if_raises_value_error_if_model_is_not_a_string(self):
        """
        Test if the GroqImageProcessor raises a ValueError if the model is not a string.
        """
        with pytest.raises(ValueError):
            GroqImageProcessor(
                groq_api_key="KEY",
                model=123,
            )   

    def test_if_raises_authentication_exception_if_api_key_is_invalid(self):
        from groq import AuthenticationError

        processor = GroqImageProcessor(
            groq_api_key="invalid",
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
                processor._get_text_from_image(image_base64="hsfjlshfjdsl")

    def test_if_raises_invalid_parameters_exception_if_model_is_invalid(self):
        """
        Test if the GroqImageProcessor raises a InvalidParametersException if the model is invalid.
        """
        processor = GroqImageProcessor(
                groq_api_key="KEY",
                model="invalid",
            )
        
        with pytest.raises(InvalidParametersException) as exc_info:
            from groq import NotFoundError
            from requests import Response
            
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
                processor._get_text_from_image(image_base64="hsfjlshfjdsl")
        
        assert exc_info.value.service_name == "Groq"
        assert exc_info.value.parameter_name == "model"
        assert exc_info.value.parameter_value == "invalid"

        assert "Groq" in str(exc_info.value)
        assert "model" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_if_raises_unexpected_image_processing_exception_if_unexpected_error_occurs_with_unexpected_error_code(self):
        """
        Test if the GroqImageProcessor raises a UnexpectedImageProcessingException if an unexpected error occurs.
        """
        processor = GroqImageProcessor(
                groq_api_key="KEY",
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )
        
        with pytest.raises(UnexpectedImageProcessingException) as exc_info:
            
            mock_response = MagicMock()
            mock_response.text = '{"error":{"code":"UNEXPECTED_ERROR","message":"Unexpected error"}}'

            with patch.object(
                processor.client.chat.completions, 
                'create', 
                side_effect=NotFoundError(
                    message="Model not found",
                    response=mock_response,
                    body='{"error":{"code":"model_not_found","message":"Model not found"}}',
                )
            ):
                processor._get_text_from_image(image_base64="hsfjlshfjdsl")
        
        assert exc_info.value.service_name == "Groq"

        assert "Groq" in str(exc_info.value)

    def test_if_raises_unexpected_captcha_solver_exception_if_unexpected_error_occurs(self):
        processor = GroqImageProcessor(
                groq_api_key="KEY",
                model="meta-llama/llama-4-scout-17b-16e-instruct",
            )
        
        with pytest.raises(UnexpectedImageProcessingException) as exc_info:
            
            mock_response = MagicMock()
            mock_response.text = '{"error":{"code":"API_REQUEST_ERROR","message":"API request error"}}'

            with patch.object(
                processor.client.chat.completions, 
                'create', 
                side_effect=Exception()
            ):
                processor._get_text_from_image(image_base64="hsfjlshfjdsl")
        
        assert exc_info.value.service_name == "Groq"

        assert "Groq" in str(exc_info.value)
            
