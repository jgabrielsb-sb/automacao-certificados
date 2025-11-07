from automacao_certificados.selenium_automations.core.interfaces import (
    ImageProcessorPort,
    CaptchaGatewayPort, FillCaptchaTextResult
)

from pydantic import BaseModel

class SolveCaptchaOutput(BaseModel):
    retries: int
    how_many_seconds: int

class SolveCaptchaService:
    def __init__(
        self,
        image_processor: ImageProcessorPort,
        captcha_gateway: CaptchaGatewayPort
    ):
        if not isinstance(image_processor, ImageProcessorPort):
            raise ValueError("image_processor must be a ImageProcessorPort")

        if not isinstance(captcha_gateway, CaptchaGatewayPort):
            raise ValueError("captcha_gateway must be a CaptchaGatewayPort")
        
        self.image_processor = image_processor
        self.captcha_gateway = captcha_gateway

    def execute(
        self,
    ) -> None:
    
        base64_img = self.captcha_gateway.get_captcha_base64_img()
        text = self.image_processor.get_text(base64_img)
        result = self.captcha_gateway.fill_captcha_text(text)

        return SolveCaptchaOutput(
            retries=result.retries,
            how_many_seconds=result.how_many_seconds,
        )


        