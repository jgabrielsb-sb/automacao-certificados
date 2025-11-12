from automacao_certificados.selenium_automations.adapters.selenium_workflow import CertidaoEstadualALSeleniumWorkflow
from automacao_certificados.selenium_automations.core.interfaces import SeleniumWorkflowInput
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver
from automacao_certificados.selenium_automations.adapters.image_processor import GroqImageProcessor
from groq import Groq
from automacao_certificados.config import settings
from automacao_certificados.selenium_automations.adapters.captcha_gateway import SeleniumCaptchaGateway
from selenium.webdriver.common.by import By
groq = Groq(api_key=settings.groq_api_key)

driver = WebDriver()

if __name__ == "__main__":
    workflow = CertidaoEstadualALSeleniumWorkflow(
        img_path_to_save_file=Path("certificado.png"),
        driver=driver,
        base_image_processor=GroqImageProcessor(client=groq),
        captcha_gateway=SeleniumCaptchaGateway(
            webdriver=driver,
            img_locator=(By.XPATH,'//div[@class="captcha-imagem"]/img'),
            input_locator=(By.XPATH,'//div[@class="captcha-texto"]/input'),
            wait_for=5
        )
    )
    workflow.get_document(
        input=SeleniumWorkflowInput(
            supplier_cnpj="60604235",
        )
    )