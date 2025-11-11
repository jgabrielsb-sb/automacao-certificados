from automacao_certificados.selenium_automations.core.interfaces import (
    SeleniumWorkflowPort,
    SeleniumWorkflowInput,
    SeleniumWorkflowOutput,

    ImageProcessorPort,
    CaptchaGatewayPort,
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
        base_image_processor: ImageProcessorPort,
        captcha_gateway: CaptchaGatewayPort,
    ):
        if not isinstance(base_image_processor, ImageProcessorPort):
            raise ValueError("base_image_processor must be a ImageProcessorPort")
        
        if not isinstance(captcha_gateway, CaptchaGatewayPort):
            raise ValueError("captcha_gateway must be a CaptchaGatewayPort")
        
        if not isinstance(img_path_to_save_file, Path):
            raise ValueError("img_path_to_save_file must be a Path")
        
        self.driver = driver
        self.base_image_processor = base_image_processor
        self.img_path_to_save_file = img_path_to_save_file
        self.captcha_gateway = captcha_gateway

    def get_document(
        self, 
        input: SeleniumWorkflowInput
    ) -> SeleniumWorkflowOutput:
        
        captcha_passed = False
        
        while not captcha_passed:
            try:
                ConsultaPage(
                    self.driver,
                    self.base_image_processor,
                    self.captcha_gateway
                ).run(
                    state_value='AL',
                    tipo_inscricao_value='CNPJ',
                    inscricao_value=input.supplier_cnpj
                )
                captcha_passed = True
            except InvalidCaptchaException:
                pass


        document_extracted, base64_pdf = DownloadPage(
            self.driver
        ).run(self.img_path_to_save_file)

        return SeleniumWorkflowOutput(
            document_extracted,
            base64_pdf
        )







