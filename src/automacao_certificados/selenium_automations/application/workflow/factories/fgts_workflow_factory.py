from .base_workflow_factory import WorkflowFactory

from automacao_certificados.selenium_automations.adapters.selenium.certidao_fgts.pages import *
from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.infra.webdriver import get_global_webdriver
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.infra.api_requester import (
    AlagoasAPIRequester,
    CertificadoAPIRequester,
    PPEAPIRequester
)

from automacao_certificados.config import settings

from groq import Groq

class FGTSWorkflowFactory(WorkflowFactory):
    def get_workflow(self) -> Workflow:
        driver = get_global_webdriver()
        http_client = HttpxClient()
        captcha_solver = ImageCaptchaSolver(
            image_processor=GroqImageProcessor(
                client=Groq(api_key=settings.groq_api_key),
            ),
            captcha_gateway=SeleniumCaptchaGateway(
                webdriver=driver,
            ),
        )
        document_downloader = DocumentFGTSDownloader(
            consulta_page=ConsultaPage(
                driver=driver,
                captcha_solver=captcha_solver
            ),
            download_page=DownloadPage(
                driver=driver
            )
        )
        certificado_api_persistance = CertificadoApiPersistance(
            api_requester=CertificadoAPIRequester(
                base_url=settings.base_certificado_api_url,
                http=http_client
            )
        )

        ppe_api_persistance = PPEPersistance(
            api_requester=PPEAPIRequester(
                http=http_client,
                api_key=settings.ppe_api_key
            )
        )

        return Workflow(
            document_downloader=document_downloader,
            certificado_api_persistance=certificado_api_persistance,
            ppe_api_persistance=ppe_api_persistance,
        )

