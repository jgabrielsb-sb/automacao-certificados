from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *
from groq import Groq, AuthenticationError, NotFoundError

SERVICE_NAME = "Groq"

class GroqImageProcessor(ImageProcessorPort):
    """
    Image processor that uses the Groq API to get the text from the image.
    It uses the meta-llama/llama-4-scout-17b-16e-instruct model by default.
    """
    def __init__(
        self,
        client: Groq,
        model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
    ):
        if not isinstance(model, str):
            raise ValueError("model must be a string")

        if not isinstance(client, Groq):
            raise ValueError("client must be a Groq client")

        super().__init__()
        
        self.client = client
        self.model = model
    
    def get_text(
        self, 
        input: ImageProcessorInput
    ) -> ImageProcessorOutput:
        try:
            base64_img = input.base64_img
            chat = self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text",
                        "text": "Read the CAPTCHA text. Return ONLY those characters (no spaces, no quotes)."},
                        {"type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
                    ],
                }],
                model=self.model,
            )

            text = chat.choices[0].message.content.strip()
            return ImageProcessorOutput(text=text)
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
            
            
        
        




