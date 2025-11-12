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

from automacao_certificados.selenium_automations.application.services import (
    SolveCaptchaService
)

from selenium.webdriver.remote.webdriver import WebDriver

from pathlib import Path

class CertidaoEstadualALSeleniumWorkflow(SeleniumWorkflowPort):
    def __init__(
        self,
        driver: WebDriver,
        img_path_to_save_file: Path,
    ):
        if not isinstance(img_path_to_save_file, Path):
            raise ValueError("img_path_to_save_file must be a Path")
        
        self.driver = driver
        self.img_path_to_save_file = img_path_to_save_file
        
    def get_document(
        self, 
        input: SeleniumWorkflowInput
    ) -> SeleniumWorkflowOutput:
        
        """
        deal with the process of consulting the cnpj cert.
        here, i would expect 
        """
        ConsultaPage(
            ...
        ).run()

        # pass the download page
        document_extracted, base64_pdf = DownloadPage(
            self.driver
        ).run(self.img_path_to_save_file)

        return SeleniumWorkflowOutput(
            document=document_extracted,
            base64_pdf=base64_pdf
        )







