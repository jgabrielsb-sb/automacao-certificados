from automacao_certificados.selenium_automations.core.interfaces import BaseImageProcessor

from groq import (
    Groq,
    AuthenticationError,
    NotFoundError,
)

from automacao_certificados.selenium_automations.adapters.image_processor.exceptions import (
    AuthenticationException,
    InvalidParametersException,
    UnexpectedImageProcessingException,
)

SERVICE_NAME = "Groq"

class GroqImageProcessor(BaseImageProcessor):
    """
    Image processor that uses the Groq API to get the text from the image.
    It uses the meta-llama/llama-4-scout-17b-16e-instruct model by default.
    """
    def __init__(
        self,
        groq_api_key: str,
        model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
    ):
        """
        Args:
            groq_api_key: The Groq API key.
            model: The model to use.
        Raises:
            ValueError: If the groq_api_key is not a string or model is not a string.
        """
        if not isinstance(groq_api_key, str):
            raise ValueError("groq_api_key must be a string")

        if not isinstance(model, str):
            raise ValueError("model must be a string")

        super().__init__()
        
        self.client = Groq(api_key=groq_api_key)
        self.model = model
    
    def _get_text_from_image(self, image_base64: str) -> str:
        """
        Gets the text from the image using the Groq API.
        Returns:
            str: The text from the image.
        Raises:
            ValueError: If the image_base64 is not a string.
            AuthenticationException: If the API key is invalid.
            InvalidParametersException: If the model is invalid.
            UnexpectedImageProcessingException: If an unexpected error occurs.
        """
        try:
            chat = self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text",
                        "text": "Read the CAPTCHA text. Return ONLY those characters (no spaces, no quotes)."},
                        {"type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ],
                }],
                model=self.model,
            )

            text = chat.choices[0].message.content.strip()
            return text
        except AuthenticationError as e: # API KEY is invalid
            raise AuthenticationException(
                service_name=SERVICE_NAME,
                original_exception=e,
            )
        except NotFoundError as e: # Not FOUND ERROR
            import json

            error_code = json.loads(e.response.text)["error"]["code"]
            if error_code == "model_not_found": # Model is invalid
                raise InvalidParametersException(
                    service_name=SERVICE_NAME,
                    parameter_name="model",
                    parameter_value=self.model,
                    original_exception=e,
                )
            else: # Another unexpected error caused by No Found
                raise UnexpectedImageProcessingException(
                    service_name=SERVICE_NAME,
                    original_exception=e,
                )

        except Exception as e: # Unhandled errors
            raise UnexpectedImageProcessingException(
                service_name=SERVICE_NAME,
                original_exception=e,
            )
            
            
        
        




