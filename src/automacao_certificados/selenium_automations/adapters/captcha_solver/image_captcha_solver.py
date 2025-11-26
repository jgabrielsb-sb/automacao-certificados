from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

class ImageCaptchaSolver(CaptchaSolverPort):
    """
    Solves the captcha by getting the captcha text from the image 
    and inserting it on the input field.
    """
    def __init__(
        self,
        image_processor: ImageProcessorPort,
        captcha_gateway: SeleniumCaptchaGatewayPort
    ):
        if not isinstance(image_processor, ImageProcessorPort):
            raise ValueError("image_processor must be a ImageProcessorPort")
        
        if not isinstance(captcha_gateway, SeleniumCaptchaGatewayPort):
            raise ValueError("captcha_gateway must be a SeleniumCaptchaGatewayPort")
        
        self.image_processor = image_processor
        self.captcha_gateway = captcha_gateway

    def solve_captcha(self, input: CaptchaSolverInput) -> None:
        base64_img = self.captcha_gateway.get_captcha_base64_img(input.img_webelement)
        text = self.image_processor.get_text(input=ImageProcessorInput(base64_img=base64_img))
        self.captcha_gateway.fill_captcha_text(input.input_webelement, text)
        return text

