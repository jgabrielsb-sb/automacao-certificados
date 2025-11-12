from automacao_certificados.selenium_automations.core.interfaces import (
    SeleniumWorkflowPort,
    SeleniumWorkflowInput,
    SeleniumWorkflowOutput,

    ImageProcessorPort,
    SeleniumCaptchaGatewayPort,
)


from automacao_certificados.selenium_automations.websites.certidao_estadual_al import (
    ConsultaPage, 
    DownloadPage
)

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import InvalidCaptchaException
from selenium.webdriver.remote.webdriver import WebDriver

from pathlib import Path

class CertidaoEstadualALSeleniumWorkflow(SeleniumWorkflowPort):
    def __init__(
        self,
        driver: WebDriver,
        img_path_to_save_file: Path,
        image_processor: ImageProcessorPort,
        captcha_gateway: SeleniumCaptchaGatewayPort,
    ):
        if not isinstance(image_processor, ImageProcessorPort):
            raise ValueError("image_processor must be a ImageProcessorPort")
        
        if not isinstance(captcha_gateway, SeleniumCaptchaGatewayPort):
            raise ValueError("captcha_gateway must be a CaptchaGatewayPort")
        
        if not isinstance(img_path_to_save_file, Path):
            raise ValueError("img_path_to_save_file must be a Path")
        
        self.driver = driver
        self.image_processor = image_processor
        self.img_path_to_save_file = img_path_to_save_file
        self.captcha_gateway = captcha_gateway

    def _solve_captcha(self, cnpj=str) -> int:
        
        captcha_passed = False
        attempts = 0
        
        while not captcha_passed:
            try:
                ConsultaPage(
                    self.driver,
                    self.image_processor,
                    self.captcha_gateway
                ).run(
                    state_value='AL',
                    tipo_inscricao_value='CNPJ',
                    inscricao_value=cnpj
                )
                captcha_passed = True
            except InvalidCaptchaException:
                attempts += 1
                pass

        return attempts


    def get_document(
        self, 
        input: SeleniumWorkflowInput
    ) -> SeleniumWorkflowOutput:

        self._solve_captcha(input.supplier_cnpj)

        document_extracted, base64_pdf = DownloadPage(
            self.driver
        ).run(self.img_path_to_save_file)

        return SeleniumWorkflowOutput(
            document=document_extracted,
            base64_pdf=base64_pdf
        )







